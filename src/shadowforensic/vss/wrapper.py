import os
import platform
import sys
from typing import List, Optional
from shadowforensic.utils.exceptions import VSSExtensionError

# Conditionally import win32 modules
try:
    if platform.system() == "Windows":
        import win32com.client
except ImportError:
    pass

class ShadowCopyInfo:
    def __init__(self, id: str, device_object: str, volume: str, created_at: str):
        self.id = id
        self.device_object = device_object
        self.volume = volume
        self.created_at = created_at

    def __repr__(self) -> str:
        return f"<ShadowCopy {self.id} on {self.volume}>"

class VSSWrapper:
    """Handles interaction with Windows Volume Shadow Copy Service."""

    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        if not self.is_windows:
            # We'll use this for development/testing on non-Windows systems
            pass

    def list_shadow_copies(self) -> List[ShadowCopyInfo]:
        """Lists all shadow copies on the system."""
        if not self.is_windows:
            return self._mock_list()

        try:
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            copies = wmi.ExecQuery("SELECT * FROM Win32_ShadowCopy")
            
            results = []
            for copy in copies:
                results.append(ShadowCopyInfo(
                    id=copy.ID,
                    device_object=copy.DeviceObject,
                    volume=copy.VolumeName,
                    created_at=copy.InstallDate
                ))
            return results
        except Exception as e:
            raise VSSExtensionError(f"Failed to list shadow copies: {e}")

    def create_shadow_copy(self, volume: str) -> str:
        """Creates a new shadow copy for the specified volume (e.g., C:\\)."""
        if not self.is_windows:
            return "MOCK-ID-123"

        try:
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            sc_class = wmi.Get("Win32_ShadowCopy")
            
            # Create method returns (Result, ShadowID)
            result, shadow_id = sc_class.Create(volume, "ClientAccessible")
            
            if result != 0:
                raise VSSExtensionError(f"Failed to create shadow copy. WMI Error code: {result}")
            
            return shadow_id
        except Exception as e:
            raise VSSExtensionError(f"Failed to create shadow copy: {e}")

    def delete_shadow_copy(self, copy_id: str) -> bool:
        """Deletes a shadow copy by its ID."""
        if not self.is_windows:
            return True

        try:
            wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            copies = wmi.ExecQuery(f"SELECT * FROM Win32_ShadowCopy WHERE ID = '{copy_id}'")
            
            for copy in copies:
                copy.Delete_()
                return True
            
            return False
        except Exception as e:
            raise VSSExtensionError(f"Failed to delete shadow copy {copy_id}: {e}")

    def _mock_list(self) -> List[ShadowCopyInfo]:
        """Returns dummy data for development on non-Windows platforms."""
        return [
            ShadowCopyInfo("{1111-2222-3333}", "\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy1", "C:\\", "2023-10-01"),
            ShadowCopyInfo("{4444-5555-6666}", "\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy2", "D:\\", "2023-11-15"),
        ]
