# Getting Started with Python UrBackup

## Installation

To install Python UrBackup, you'll need Python installed on your system. Python UrBackup supports Python 3.x.

```bash
pip install python-urbackup
```

## Configuration

After installation, you'll need to configure the library with your UrBackup server details:

```python
from urbackup import urbackup_server

server = urbackup_server('your_server_url', 'your_username', 'your_password')
```

This is the basic configuration needed to start interacting with your UrBackup server.