# Python UrBackup [![urbackup.org](docs/urbackup.png)](https://www.urbackup.org/)

[![PyPI](https://img.shields.io/pypi/v/python-urbackup)](https://pypi.org/project/python-urbackup/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-urbackup)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/judahpaul16/python-urbackup/workflow.yaml)](https://github.com/judahpaul16/python-urbackup/actions)
[![Coverage Status](https://coveralls.io/repos/github/judahpaul16/python-urbackup/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/judahpaul16/python-urbackup?branch=master)
[![Documentation Status](https://readthedocs.org/projects/python-urbackup/badge/?version=latest)](https://python-urbackup.readthedocs.io/en/latest/?badge=latest)

Python wrapper to interact with UrBackup servers. Manage backups, restore operations, and monitor server status programmatically.

*Originally [urbackup-server-web-api-wrapper](https://github.com/uroni/urbackup-server-python-web-api-wrapper)*

## Installation

```bash
pip install python-urbackup
```

## Quick Start

```python
from urbackup import urbackup_server

server = urbackup_server("http://127.0.0.1:55414/x", "admin", "password")

if server.login():
    print("Connected!")
```

## Legacy API (dict-based)

The legacy API returns raw dicts/lists, preserving backward compatibility.

```python
from urbackup import urbackup_server

server = urbackup_server("http://127.0.0.1:55414/x", "admin", "password")

# Client status
clients = server.get_status()
for client in clients:
    print(f"{client['name']}: online={client['online']}")

# Start backups
server.start_incr_file_backup("my-client")
server.start_full_image_backup("my-client")

# Settings
settings = server.get_global_settings()
server.set_global_setting("backup_window", "1-5/8-17")

# Client settings
server.change_client_setting("my-client", "internet_speed", "50000")

# Extra clients
server.add_extra_client("10.0.0.5")
extras = server.get_extra_clients()

# Monitor actions
actions = server.get_actions()
for action in actions or []:
    server.stop_action(action)

# Live log
log = server.get_livelog()
```

## Typed API (dataclass-based)

The typed API returns structured dataclass objects with full type hints.

```python
from urbackup import urbackup_server, BackupType, ClientNotFoundError

server = urbackup_server("http://127.0.0.1:55414/x", "admin", "password")
server.login()

# Typed client statuses
clients = server.get_client_statuses()
for client in clients:
    print(f"{client.name}: id={client.id}, online={client.online}")

# Find specific client (raises ClientNotFoundError if missing)
try:
    client = server.get_client_status_by_name("my-client")
    print(f"Last backup: {client.lastbackup}")
except ClientNotFoundError:
    print("Client not found")

# Start backup with enum
server.start_backup_typed("my-client", BackupType.INCR_FILE)

# Typed usage stats
for entry in server.get_usage_typed():
    print(f"{entry.name}: {entry.used} bytes, {entry.files} files")

# Typed actions with progress
for action in server.get_actions_typed():
    print(f"Client {action.clientid}: {action.progress_percent}%")

# Typed settings (raises AccessDeniedError on failure)
settings = server.get_global_settings_typed()
server.set_global_setting_typed("backup_window", "1-7/0-24")

# Client settings (raises KeyError for invalid keys)
server.change_client_setting_typed("my-client", "internet_speed", "50000")

# Typed log entries
for entry in server.get_livelog_typed():
    print(f"[{entry.level}] {entry.message}")

# Backup history
backups = server.get_backups(clientid=1)
images = server.get_image_backups(clientid=1)

# Extra clients
for ec in server.get_extra_clients_typed():
    print(f"{ec.hostname} (id={ec.id})")

# Server identity
identity = server.get_server_identity_str()
```

## Settings Example

Configure a client's backup folder path and incremental backup interval:

```python
server.change_client_setting("my-client", "default_dirs", "/home;/etc")
server.change_client_setting("my-client", "update_freq_incr", "4")  # hours
```

## Basic Auth (htpasswd)

If your server uses HTTP basic authentication:

```python
server = urbackup_server(
    "http://127.0.0.1:55414/x", "admin", "password",
    basic_username="httpuser", basic_password="httppass",
)
```

## Exception Hierarchy

```
UrbackupError
├── AuthenticationError    # login failed
├── ClientNotFoundError    # client name not found
├── AccessDeniedError      # insufficient permissions
└── UserAlreadyExistsError # duplicate user creation
```

## Available Types

| Type | Description |
|------|-------------|
| `ClientStatus` | Client info: id, name, online, lastbackup, ip, etc. |
| `BackupEntry` | Backup record: id, clientid, backuptime, size_bytes |
| `UsageEntry` | Storage usage: name, used, files, images |
| `ActionProgress` | Running action: clientid, id, action, progress_percent |
| `LogEntry` | Log record: id, message, level, time |
| `ExtraClient` | Extra client: id, hostname |
| `User` | User account: id, name, rights |
| `Group` | Client group: id, name |
| `BackupType` | Enum: INCR_FILE, FULL_FILE, INCR_IMAGE, FULL_IMAGE |
| `ActionType` | IntEnum: all server action type constants |
| `InstallerOS` | Enum: WINDOWS, LINUX |
| `LogLevel` | IntEnum: ERROR, WARNING, INFO, DEBUG |

All dataclasses include a `raw` field with the original API dict.

## UrBackup CLI <img src="data:image/svg+xml,<svg fill='%234D4D4D' role='img' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><title>Windows Terminal</title><path d='M8.165 6V3h7.665v3H8.165zm-.5-3H1c-.55 0-1 .45-1 1v2h7.665V3zM23 3h-6.67v3H24V4c0-.55-.45-1-1-1zM0 6.5h24V20c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V6.5zM11.5 18c0 .3.2.5.5.5h8c.3 0 .5-.2.5-.5v-1.5c0-.3-.2-.5-.5-.5h-8c-.3 0-.5.2-.5.5V18zm-5.2-4.55l-3.1 3.1c-.25.25-.25.6 0 .8l.9.9c.25.25.6.25.8 0l4.4-4.4a.52.52 0 0 0 0-.8l-4.4-4.4c-.2-.2-.6-.2-.8 0l-.9.9c-.25.2-.25.55 0 .8l3.1 3.1z'/></svg>" width=20>

The UrBackup CLI is a command-line interface that allows you to interact with the UrBackup server from a client machine.

*Important Note: For Windows the command-line tool is `urbackupclient_cmd`. Mac and Linux use `urbackupclientctl`.*

CLI options for `urbackupclientctl` and `urbackupclient_cmd` are as follows:

```sh
USAGE:

        urbackupclientctl [--help] [--version] <command> [<args>]

Get specific command help with urbackupclientctl <command> --help

        urbackupclientctl start
                Start an incremental/full image/file backup

        urbackupclientctl status
                Get current backup status

        urbackupclientctl browse
                Browse backups and files/folders in backups

        urbackupclientctl restore-start
                Restore files/folders from backup

        urbackupclientctl set-settings
                Set backup settings

        urbackupclientctl reset-keep
                Reset keeping files during incremental backups

        urbackupclientctl add-backupdir
                Add new directory to backup set

        urbackupclientctl list-backupdirs
                List directories that are being backed up

        urbackupclientctl remove-backupdir
                Remove directory from backup set
```

For more information, please refer to the [UrBackup Administration Documentation](https://www.urbackup.org/administration_manual.html).

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
