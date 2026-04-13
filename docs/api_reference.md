# API Reference

## `urbackup_server`

The main class for interacting with a UrBackup server. Inherits both the legacy (dict-returning) and typed (dataclass-returning) APIs.

### Constructor

```python
urbackup_server(
    url: str,
    username: str,
    password: str,
    *,
    basic_username: str = "",
    basic_password: str = "",
)
```

| Parameter | Description |
|-----------|-------------|
| `url` | Server URL (e.g. `http://127.0.0.1:55414/x`) |
| `username` | UrBackup admin username |
| `password` | UrBackup admin password |
| `basic_username` | Optional HTTP basic auth username (for .htpasswd) |
| `basic_password` | Optional HTTP basic auth password |

### Authentication

- `login() -> bool`: Log in to the server. Tries anonymous login first, falls back to username/password with MD5 or PBKDF2 hashing.

### Legacy API (dict-returning)

These methods return raw dicts/lists or `None` on failure.

| Method | Returns | Description |
|--------|---------|-------------|
| `get_status()` | `list[dict] \| None` | All client statuses |
| `get_client_status(clientname)` | `dict \| None` | Single client status |
| `get_server_identity()` | `str \| None` | Server identity string |
| `get_usage()` | `list[dict] \| None` | Storage usage per client |
| `get_actions()` | `list[dict] \| None` | Currently running actions |
| `get_livelog(clientid=0)` | `list[dict] \| None` | Live log entries |
| `get_extra_clients()` | `list[dict] \| None` | Extra clients list |
| `get_global_settings()` | `dict \| None` | Global server settings |
| `get_client_settings(clientname)` | `dict \| None` | Settings for a client |
| `get_client_authkey(clientname)` | `str \| None` | Client internet auth key |
| `set_global_setting(key, new_value)` | `bool` | Update a global setting |
| `change_client_setting(clientname, key, new_value)` | `bool` | Update a client setting |
| `add_client(clientname)` | `dict \| None` | Add a new client |
| `add_extra_client(addr)` | `bool` | Add an extra client by hostname |
| `remove_extra_client(ecid)` | `bool` | Remove an extra client |
| `start_incr_file_backup(clientname)` | `bool` | Start incremental file backup |
| `start_full_file_backup(clientname)` | `bool` | Start full file backup |
| `start_incr_image_backup(clientname)` | `bool` | Start incremental image backup |
| `start_full_image_backup(clientname)` | `bool` | Start full image backup |
| `stop_action(action)` | `bool` | Stop a running action |
| `download_installer(installer_fn, new_clientname, os='linux')` | `bool` | Download client installer |

### Typed API (dataclass-returning)

These methods return structured dataclass objects and raise exceptions on failure.

| Method | Returns | Description |
|--------|---------|-------------|
| `get_client_statuses()` | `list[ClientStatus]` | All client statuses |
| `get_client_status_by_name(clientname)` | `ClientStatus` | Single client (raises `ClientNotFoundError`) |
| `get_server_identity_str()` | `str` | Server identity string |
| `get_usage_typed()` | `list[UsageEntry]` | Storage usage per client |
| `get_actions_typed()` | `list[ActionProgress]` | Currently running actions |
| `get_livelog_typed(clientid=0)` | `list[LogEntry]` | Live log entries |
| `get_extra_clients_typed()` | `list[ExtraClient]` | Extra clients list |
| `get_backups(clientid)` | `list[BackupEntry]` | File backups for a client |
| `get_image_backups(clientid)` | `list[BackupEntry]` | Image backups for a client |
| `get_global_settings_typed()` | `dict` | Global settings (raises `AccessDeniedError`) |
| `set_global_setting_typed(key, value)` | `bool` | Update a global setting |
| `get_client_settings_typed(clientname)` | `dict` | Client settings (raises `AccessDeniedError`) |
| `change_client_setting_typed(clientname, key, new_value)` | `bool` | Update a client setting (raises `KeyError`) |
| `start_backup_typed(clientname, backup_type)` | `bool` | Start backup with `BackupType` enum |
| `stop_action_typed(action)` | `bool` | Stop a running `ActionProgress` |
| `get_users()` | `list[User]` | List server users |
| `get_groups()` | `list[Group]` | List client groups |
| `add_user(username, password, rights='all')` | `bool` | Add user (raises `UserAlreadyExistsError`) |
| `download_installer_typed(installer_fn, new_clientname, os=InstallerOS.LINUX)` | `bool` | Download client installer |

## Exceptions

All exceptions inherit from `UrbackupError`.

| Exception | Raised when |
|-----------|-------------|
| `AuthenticationError` | Login fails |
| `ClientNotFoundError` | Client name not found on server |
| `AccessDeniedError` | Insufficient permissions for the operation |
| `UserAlreadyExistsError` | Attempting to create a duplicate user |

## Data Types

### `ClientStatus`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Client ID |
| `name` | `str` | Client name |
| `online` | `bool` | Whether client is online |
| `lastbackup` | `int` | Last file backup timestamp |
| `lastbackup_image` | `int` | Last image backup timestamp |
| `file_ok` | `bool` | File backup status OK |
| `image_ok` | `bool` | Image backup status OK |
| `ip` | `str` | Client IP address |
| `client_version_string` | `str` | Client software version |
| `os_version_string` | `str` | Client OS version |
| `raw` | `dict` | Original API response dict |

### `BackupEntry`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Backup ID |
| `clientid` | `int` | Client ID |
| `backuptime` | `int` | Backup timestamp |
| `incremental` | `int` | Whether backup is incremental |
| `size_bytes` | `int` | Backup size in bytes |
| `raw` | `dict` | Original API response dict |

### `UsageEntry`

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Client name |
| `used` | `int` | Bytes used |
| `files` | `int` | Number of file backups |
| `images` | `int` | Number of image backups |
| `raw` | `dict` | Original API response dict |

### `ActionProgress`

| Field | Type | Description |
|-------|------|-------------|
| `clientid` | `int` | Client ID |
| `id` | `int` | Action ID |
| `name` | `str` | Client name |
| `action` | `int` | Action type constant |
| `progress_percent` | `int` | Progress percentage (-1 if unknown) |
| `raw` | `dict` | Original API response dict |

### `LogEntry`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Log entry ID |
| `message` | `str` | Log message |
| `level` | `int` | Log level (see `LogLevel`) |
| `time` | `int` | Timestamp |
| `raw` | `dict` | Original API response dict |

### `ExtraClient`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Extra client ID |
| `hostname` | `str` | Hostname or IP |
| `raw` | `dict` | Original API response dict |

### `User`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | User ID |
| `name` | `str` | Username |
| `rights` | `str` | Permission rights string |
| `raw` | `dict` | Original API response dict |

### `Group`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Group ID |
| `name` | `str` | Group name |
| `raw` | `dict` | Original API response dict |

## Enums

### `BackupType`

| Value | Description |
|-------|-------------|
| `INCR_FILE` | Incremental file backup |
| `FULL_FILE` | Full file backup |
| `INCR_IMAGE` | Incremental image backup |
| `FULL_IMAGE` | Full image backup |

### `ActionType`

Integer enum of all server action type constants: `INCR_FILE` (1), `FULL_FILE` (2), `INCR_IMAGE` (3), `FULL_IMAGE` (4), `RESUMED_INCR_FILE` (5), `RESUMED_FULL_FILE` (6), `FILE_RESTORE` (8), `IMAGE_RESTORE` (9), `CLIENT_UPDATE` (10), `CHECK_DB_INTEGRITY` (11), `BACKUP_DB` (12), `RECALC_STATS` (13).

### `InstallerOS`

| Value | Description |
|-------|-------------|
| `WINDOWS` | Windows installer |
| `LINUX` | Linux installer |

### `LogLevel`

| Value | Description |
|-------|-------------|
| `ERROR` (1) | Error messages |
| `WARNING` (2) | Warning messages |
| `INFO` (3) | Informational messages |
| `DEBUG` (4) | Debug messages |

For more information on the UrBackup server API, refer to the [official UrBackup documentation](https://www.urbackup.org/administration_manual.html).
