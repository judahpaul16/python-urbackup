# Python UrBackup ![Icon](https://www.urbackup.org/favicon.ico)

Python UrBackup is a powerful Python wrapper designed to interact with UrBackup servers. This library allows you to manage backups, restore operations, and monitor the server status programmatically.

## Features

- Easy to use Python API.
- Manage and monitor UrBackup server operations.
- Download and configure client installers.

## Installation

```bash
pip install python-urbackup
```

For more detailed installation instructions, see the [Getting Started](getting_started.md) section.

## Quick Start

Here's a quick example to get you started:

```python
from urbackup import urbackup_server

# Initialize and log in
server = urbackup_server('your_server_url', 'your_username', 'your_password')
if server.login():
    print("Login successful!")
```

For more examples and usage instructions, visit the [Usage](usage/initialization.md) section.
