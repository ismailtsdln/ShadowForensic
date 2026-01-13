import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from shadowforensic import __version__
from shadowforensic.vss.wrapper import VSSWrapper
from shadowforensic.core.mounter import ShadowMounter
from shadowforensic.core.scanner import FileScanner, RecoveryOptions
from shadowforensic.utils.exceptions import ShadowForensicError
from loguru import logger
import sys

# Brand Banner
BRAND_BANNER = """
 ██████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
╚█████╗ ███████║███████║██║  ██║██║   ██║██║ █╗ ██║
 ╚═══██╗██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
██████╔╝██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ 
                   ███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗███████╗██╗ ██████╗
                   ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██║██╔════╝
                   █████╗  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████╗██║██║     
                   ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║╚════██║██║██║     
                   ██║     ╚██████╔╝██║  ██║███████╗██║ ╚████║███████║██║╚██████╗
                   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝
"""

# Configure logger
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")

app = typer.Typer(
    name="shadowforensic",
    help="Professional Windows VSS Forensic Tool",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()
vss = VSSWrapper()

def show_banner():
    banner_text = Text(BRAND_BANNER, style="bold cyan")
    sub_text = Text(f"\nVersion: {__version__} | Professional VSS Forensic Tool\n", style="italic dim white")
    console.print(Panel.fit(Text.assemble(banner_text, sub_text), border_style="blue", padding=(1, 4)))

@app.command()
def list():
    """List all existing Volume Shadow Copies."""
    try:
        copies = vss.list_shadow_copies()
        if not copies:
            console.print("[yellow]No shadow copies found.[/yellow]")
            return

        table = Table(title="Volume Shadow Copies")
        table.add_column("ID", style="cyan")
        table.add_column("Volume", style="green")
        table.add_column("Created At", style="magenta")
        table.add_column("Device Object", style="dim")

        for copy in copies:
            table.add_row(copy.id, copy.volume, copy.created_at, copy.device_object)

        console.print(table)
    except ShadowForensicError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def create(drive: str = typer.Argument(..., help="The drive letter (e.g., C:\\)")):
    """Create a new Volume Shadow Copy."""
    try:
        console.print(f"[bold green]Creating Shadow Copy for {drive}...[/bold green]")
        shadow_id = vss.create_shadow_copy(drive)
        console.print(f"[bold green]Successfully created shadow copy:[/bold green] {shadow_id}")
    except ShadowForensicError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def mount(
    copy_id: str = typer.Argument(..., help="ID of the shadow copy"),
    path: str = typer.Argument(..., help="Mount point path (e.g., C:\\mnt\\shadow_1)"),
):
    """Mount a Shadow Copy to a local path."""
    try:
        copies = vss.list_shadow_copies()
        target_copy = next((c for c in copies if c.id == copy_id), None)
        
        if not target_copy:
            console.print(f"[bold red]Error:[/bold red] Shadow copy {copy_id} not found.")
            raise typer.Exit(code=1)

        console.print(f"[bold magenta]Mounting {copy_id} to {path}...[/bold magenta]")
        ShadowMounter.mount(target_copy.device_object, path)
        console.print(f"[bold green]Successfully mounted to {path}[/bold green]")
    except ShadowForensicError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def unmount(path: str = typer.Argument(..., help="Path to unmount")):
    """Unmount a previously mounted Shadow Copy."""
    try:
        console.print(f"[bold yellow]Unmounting {path}...[/bold yellow]")
        ShadowMounter.unmount(path)
        console.print("[bold green]Successfully unmounted.[/bold green]")
    except ShadowForensicError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def recover(
    copy_id: str = typer.Argument(..., help="ID of the shadow copy"),
    output: str = typer.Option("./recovered", help="Output directory"),
    filter: str = typer.Option("*", help="File filter pattern (e.g., *.docx)"),
):
    """Recover files from a Shadow Copy."""
    import tempfile
    
    try:
        copies = vss.list_shadow_copies()
        target_copy = next((c for c in copies if c.id == copy_id), None)
        
        if not target_copy:
            console.print(f"[bold red]Error:[/bold red] Shadow copy {copy_id} not found.")
            raise typer.Exit(code=1)

        # Temporary mount for recovery
        with tempfile.TemporaryDirectory() as temp_mount_base:
            # Note: TemporaryDirectory creates a dir, but ShadowMounter expects to CREATE the symlink at 'path'.
            # So we use a subpath.
            mount_path = os.path.join(temp_mount_base, "mnt")
            
            console.print(f"[bold cyan]Recovering files from {copy_id}...[/bold cyan]")
            ShadowMounter.mount(target_copy.device_object, mount_path)
            
            options = RecoveryOptions(filters=[filter])
            scanner = FileScanner(mount_path, output, options)
            scanner.run()
            
            ShadowMounter.unmount(mount_path)
            
        console.print(f"[bold green]Recovery completed to {output}[/bold green]")
    except ShadowForensicError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

def version_callback(value: bool):
    if value:
        console.print(f"ShadowForensic version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show version and exit"
    )
):
    """
    ShadowForensic: High-performance Windows Volume Shadow Copy analysis tool.
    """
    show_banner()

if __name__ == "__main__":
    app()
