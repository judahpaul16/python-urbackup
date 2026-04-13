# Operations

## Legacy API (dict-based)

### Getting Client Status

```python
client_status = server.get_client_status("client_name")
if client_status:
    print(f"Client status: {client_status}")
```

### Starting Backups

```python
server.start_incr_file_backup("client_name")
server.start_full_file_backup("client_name")
server.start_incr_image_backup("client_name")
server.start_full_image_backup("client_name")
```

### Settings

```python
settings = server.get_global_settings()
server.set_global_setting("backup_window", "1-5/8-17")

server.change_client_setting("client_name", "default_dirs", "/home;/etc")
server.change_client_setting("client_name", "update_freq_incr", "4")
```

### Managing Clients

```python
new_client = server.add_client("new_client_name")

server.add_extra_client("10.0.0.5")
extras = server.get_extra_clients()
```

### Monitoring

```python
actions = server.get_actions()
for action in actions or []:
    server.stop_action(action)

log = server.get_livelog()
usage = server.get_usage()
```

### Download Installer

```python
server.download_installer("installer.sh", "new_client", os="linux")
```

## Typed API (dataclass-based)

The typed API returns structured dataclass objects and raises exceptions instead of returning `None`.

### Client Status

```python
from urbackup import ClientNotFoundError

clients = server.get_client_statuses()
for client in clients:
    print(f"{client.name}: id={client.id}, online={client.online}")

try:
    client = server.get_client_status_by_name("my-client")
    print(f"Last backup: {client.lastbackup}")
except ClientNotFoundError:
    print("Client not found")
```

### Starting Backups

```python
from urbackup import BackupType

server.start_backup_typed("client_name", BackupType.INCR_FILE)
server.start_backup_typed("client_name", BackupType.FULL_IMAGE)
```

### Backup History

```python
backups = server.get_backups(clientid=1)
for b in backups:
    print(f"Backup {b.id}: {b.size_bytes} bytes at {b.backuptime}")

images = server.get_image_backups(clientid=1)
```

### Settings

```python
settings = server.get_global_settings_typed()
server.set_global_setting_typed("backup_window", "1-7/0-24")

client_settings = server.get_client_settings_typed("my-client")
server.change_client_setting_typed("my-client", "internet_speed", "50000")
```

### Monitoring

```python
for action in server.get_actions_typed():
    print(f"Client {action.clientid}: {action.progress_percent}%")
    server.stop_action_typed(action)

for entry in server.get_livelog_typed():
    print(f"[{entry.level}] {entry.message}")

for entry in server.get_usage_typed():
    print(f"{entry.name}: {entry.used} bytes")
```

### Extra Clients

```python
for ec in server.get_extra_clients_typed():
    print(f"{ec.hostname} (id={ec.id})")
```

### Users and Groups

```python
from urbackup import UserAlreadyExistsError

users = server.get_users()
groups = server.get_groups()

try:
    server.add_user("newadmin", "password123")
except UserAlreadyExistsError:
    print("User already exists")
```

### Download Installer

```python
from urbackup import InstallerOS

server.download_installer_typed("installer.sh", "new_client", os=InstallerOS.LINUX)
```
