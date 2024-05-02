# Initialization

To start using the Python UrBackup API, you need to initialize the `Server` object:

```python
from urbackup import Server

server = Server('your_server_url', 'your_username', 'your_password')
```

## Logging In

Once the server object is initialized, log in to perform operations:

```python
if server.login():
    print("Login successful!")
else:
    print("Login failed!")
```