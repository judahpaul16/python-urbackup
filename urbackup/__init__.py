from ._legacy import _LegacyAPI
from ._typed import _TypedAPI
from ._types import (
    AccessDeniedError,
    ActionProgress,
    ActionType,
    AuthenticationError,
    BackupEntry,
    BackupType,
    ClientNotFoundError,
    ClientStatus,
    ExtraClient,
    Group,
    InstallerOS,
    LogEntry,
    LogLevel,
    UrbackupError,
    UsageEntry,
    User,
    UserAlreadyExistsError,
    installer_os,
)


class urbackup_server(_LegacyAPI, _TypedAPI):
    pass


__all__ = [
    "urbackup_server",
    "AccessDeniedError",
    "ActionProgress",
    "ActionType",
    "AuthenticationError",
    "BackupEntry",
    "BackupType",
    "ClientNotFoundError",
    "ClientStatus",
    "ExtraClient",
    "Group",
    "InstallerOS",
    "LogEntry",
    "LogLevel",
    "UrbackupError",
    "UsageEntry",
    "User",
    "UserAlreadyExistsError",
    "installer_os",
]
