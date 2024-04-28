# Operations

## Getting Client Status

To get the status of a specific client:

```python
client_status = server.get_client_status('client_name')
if client_status:
    print(f"Client status: {client_status}")
else:
    print("Client not found or access denied.")
```

## Downloading an Installer

To download an installer for a new client:

```python
if server.download_installer('path/to/installer', 'new_client_name'):
    print("Installer downloaded successfully.")
else:
    print("Failed to download installer.")
```

## Starting Backups

Start an incremental file backup:

```python
if server.start_incr_file_backup('client_name'):
    print("Incremental file backup started successfully.")
```

## Managing Clients

Add a new client to the server:

```python
new_client = server.add_client('new_client_name')
if new_client:
    print("New client added:", new_client)
else:
    print("Failed to add new client.")
```