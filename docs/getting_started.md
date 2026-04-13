# Getting Started

## Requirements

Python 3.10 or later.

## Installation

```bash
pip install python-urbackup
```

## Configuration

```python
from urbackup import urbackup_server

server = urbackup_server("http://127.0.0.1:55414/x", "admin", "password")
```

If your server uses HTTP basic authentication (.htpasswd):

```python
server = urbackup_server(
    "http://127.0.0.1:55414/x", "admin", "password",
    basic_username="httpuser", basic_password="httppass",
)
```

## Logging In

```python
if server.login():
    print("Login successful!")
else:
    print("Login failed!")
```

Login is called automatically by all API methods, but you can call it explicitly to verify connectivity.
