from typer.testing import CliRunner
from shadowforensic.cli.main import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "ShadowForensic version:" in result.stdout

def test_list():
    # This should work on any OS due to mock fallback in VSSWrapper
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Volume Shadow Copies" in result.stdout
    assert "{1111-2222-3333}" in result.stdout

def test_create_mock():
    result = runner.invoke(app, ["create", "C:"])
    assert result.exit_code == 0
    assert "Successfully created shadow copy: MOCK-ID-123" in result.stdout
