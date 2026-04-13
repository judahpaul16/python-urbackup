from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, Enum
from typing import Any


class InstallerOS(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"


class BackupType(str, Enum):
    INCR_FILE = "incr_file"
    FULL_FILE = "full_file"
    INCR_IMAGE = "incr_image"
    FULL_IMAGE = "full_image"


class ActionType(IntEnum):
    INCR_FILE = 1
    FULL_FILE = 2
    INCR_IMAGE = 3
    FULL_IMAGE = 4
    RESUMED_INCR_FILE = 5
    RESUMED_FULL_FILE = 6
    FILE_RESTORE = 8
    IMAGE_RESTORE = 9
    CLIENT_UPDATE = 10
    CHECK_DB_INTEGRITY = 11
    BACKUP_DB = 12
    RECALC_STATS = 13


class LogLevel(IntEnum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4


installer_os = InstallerOS


class UrbackupError(Exception):
    pass


class AuthenticationError(UrbackupError):
    pass


class ClientNotFoundError(UrbackupError):
    pass


class AccessDeniedError(UrbackupError):
    pass


class UserAlreadyExistsError(UrbackupError):
    pass


@dataclass
class ClientStatus:
    id: int
    name: str
    online: bool = False
    lastbackup: int = 0
    lastbackup_image: int = 0
    file_ok: bool = False
    image_ok: bool = False
    ip: str = ""
    client_version_string: str = ""
    os_version_string: str = ""
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ClientStatus:
        return cls(
            id=data["id"],
            name=data["name"],
            online=data.get("online", False),
            lastbackup=data.get("lastbackup", 0),
            lastbackup_image=data.get("lastbackup_image", 0),
            file_ok=data.get("file_ok", False),
            image_ok=data.get("image_ok", False),
            ip=data.get("ip", ""),
            client_version_string=data.get("client_version_string", ""),
            os_version_string=data.get("os_version_string", ""),
            raw=data,
        )


@dataclass
class BackupEntry:
    id: int
    clientid: int
    backuptime: int
    incremental: int = 0
    size_bytes: int = 0
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BackupEntry:
        return cls(
            id=data["id"],
            clientid=data.get("clientid", 0),
            backuptime=data.get("backuptime", 0),
            incremental=data.get("incremental", 0),
            size_bytes=data.get("size_bytes", 0),
            raw=data,
        )


@dataclass
class UsageEntry:
    name: str
    used: int = 0
    files: int = 0
    images: int = 0
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UsageEntry:
        return cls(
            name=data.get("name", ""),
            used=data.get("used", 0),
            files=data.get("files", 0),
            images=data.get("images", 0),
            raw=data,
        )


@dataclass
class LogEntry:
    id: int
    message: str
    level: int = 0
    time: int = 0
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LogEntry:
        return cls(
            id=data["id"],
            message=data.get("msg", data.get("message", "")),
            level=data.get("loglevel", data.get("level", 0)),
            time=data.get("time", 0),
            raw=data,
        )


@dataclass
class ActionProgress:
    clientid: int
    id: int
    name: str = ""
    action: int = 0
    progress_percent: int = -1
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ActionProgress:
        return cls(
            clientid=data["clientid"],
            id=data["id"],
            name=data.get("name", ""),
            action=data.get("action", 0),
            progress_percent=data.get("pcdone", data.get("progress_percent", -1)),
            raw=data,
        )


@dataclass
class ExtraClient:
    id: int
    hostname: str
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExtraClient:
        return cls(
            id=data["id"],
            hostname=data.get("hostname", ""),
            raw=data,
        )


@dataclass
class User:
    id: int
    name: str
    rights: str = ""
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls(
            id=data["id"],
            name=data["name"],
            rights=data.get("rights", ""),
            raw=data,
        )


@dataclass
class Group:
    id: int
    name: str
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Group:
        return cls(
            id=data["id"],
            name=data["name"],
            raw=data,
        )
