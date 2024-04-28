# Initialization

To start using the Python UrBackup API, you need to initialize the `urbackup_server` object:

```python
from urbackup import urbackup_server

server = urbackup_server('your_server_url', 'your_username', 'your_password')
```

## Logging In

Once the server object is initialized, log in to perform operations:

```python
if server.login():
    print("Login successful!")
else:
    print("Login failed!")
```