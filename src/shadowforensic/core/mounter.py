import os
import platform
import subprocess
from shadowforensic.utils.exceptions import MountError

class ShadowMounter:
    """Handles mounting and unmounting of shadow copies."""

    @staticmethod
    def mount(device_object: str, mount_point: str) -> bool:
        """
        Mounts a shadow copy device object to a local directory.
        Uses symbolic links on Windows.
        """
        if platform.system() != "Windows":
            print(f"MOCK: Mounting {device_object} to {mount_point}")
            # Ensure parent directory exists for mock
            os.makedirs(os.path.dirname(mount_point), exist_ok=True)
            with open(mount_point + ".mock", "w") as f:
                f.write(f"Mounted: {device_object}")
            return True

        # Append trailing slash to device object if missing for Windows symbolic links
        if not device_object.endswith("\\"):
            device_object += "\\"

        try:
            # We use subprocess to call mklink /D because os.symlink might require 
            # specific privileges or behave differently with globalroot paths.
            # Command: mklink /D mount_point device_object
            # Note: Requires Administrator privileges.
            cmd = f'mklink /D "{mount_point}" "{device_object}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise MountError(f"Failed to mount shadow copy: {result.stderr}")
            
            return True
        except Exception as e:
            raise MountError(f"Error during mount operation: {e}")

    @staticmethod
    def unmount(mount_point: str) -> bool:
        """
        Unmounts a shadow copy by removing the symbolic link.
        """
        if platform.system() != "Windows":
            print(f"MOCK: Unmounting {mount_point}")
            if os.path.exists(mount_point + ".mock"):
                os.remove(mount_point + ".mock")
            return True

        try:
            if os.path.islink(mount_point) or os.path.exists(mount_point):
                # On Windows, deleting a directory symlink is done with 'rmdir'
                # or just removing the file/link entry.
                if os.path.isdir(mount_point):
                    os.rmdir(mount_point)
                else:
                    os.remove(mount_point)
                return True
            return False
        except Exception as e:
            raise MountError(f"Failed to unmount {mount_point}: {e}")
