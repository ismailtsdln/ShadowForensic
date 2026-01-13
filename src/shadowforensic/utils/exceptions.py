class ShadowForensicError(Exception):
    """Base exception for ShadowForensic."""
    pass

class VSSExtensionError(ShadowForensicError):
    """Raised when VSS system calls fail."""
    pass

class MountError(ShadowForensicError):
    """Raised when mounting or unmounting fails."""
    pass

class RecoveryError(ShadowForensicError):
    """Raised during file recovery operations."""
    pass
