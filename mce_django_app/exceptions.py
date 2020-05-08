__all__ = [
    'ResourceTypeNotFound',
    'DisableSyncError',
    'ProviderNotFound',
    'RegionNotFound',
]

class ResourceTypeNotFound(Exception):
    pass

class DisableSyncError(Exception):
    """Synchronization Disable"""

class ProviderNotFound(Exception):
    pass

class RegionNotFound(Exception):
    pass

