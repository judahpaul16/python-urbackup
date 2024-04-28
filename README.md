# Python UrBackup [![urbackup.org](docs/urbackup.png)](https://www.urbackup.org/)

[![PyPI](https://img.shields.io/pypi/v/python-urbackup)](https://pypi.org/project/python-urbackup/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dirconfig)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/judahpaul16/python-urbackup/workflow.yaml)](https://github.com/judahpaul16/python-urbackup/actions)
[![Coverage Status](https://coveralls.io/repos/github/judahpaul16/python-urbackup/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/judahpaul16/python-urbackup?branch=master)
[![Documentation Status](https://readthedocs.org/projects/python-urbackup/badge/?version=latest)](https://python-urbackup.readthedocs.io/en/latest/?badge=latest)

Python UrBackup is a powerful Python wrapper designed to interact with UrBackup servers. This library allows you to manage backups, restore operations, and monitor the server status programmatically.

*Originally [urbackup-server-web-api-wrapper](https://github.com/uroni/urbackup-server-python-web-api-wrapper)*

## Installation

Install with:

	pip3 install python-urbackup

To update the "Usage" section of your GitHub README, we can provide a more detailed and structured snippet that reflects the initialization, login, and some common operations with the `urbackup_server` class. Here is the revised "Usage" section that can be added:

## Usage

### Initialization

Create an instance of the `urbackup_server` by specifying the server URL, username, and password. Replace `'your_server_url'`, `'your_username'`, and `'your_password'` with your server details:

```python
from urbackup import urbackup_server

backup_server = urbackup_server('your_server_url', 'your_username', 'your_password')
```

### Logging In

To perform any operations, you need to log in:

```python
if backup_server.login():
    print("Login successful!")
else:
    print("Login failed!")
```

### Getting Client Status

Retrieve the status of a specific client:

```python
client_status = backup_server.get_client_status('client_name')
if client_status:
    print(f"Client status: {client_status}")
else:
    print("Client not found or access denied.")
```

### Downloading an Installer

To download an installer for a new client, specify the file path and the client's name:

```python
if backup_server.download_installer('path/to/installer', 'new_client_name'):
    print("Installer downloaded successfully.")
else:
    print("Failed to download installer.")
```

### Starting Backups

You can start different types of backups for a client. Here are examples of starting an incremental file backup and a full file backup:

```python
if backup_server.start_incr_file_backup('client_name'):
    print("Incremental file backup started successfully.")
else:
    print("Failed to start incremental file backup.")

if backup_server.start_full_file_backup('client_name'):
    print("Full file backup started successfully.")
else:
    print("Failed to start full file backup.")
```

### Managing Clients

Add a new client to the server:

```python
new_client = backup_server.add_client('new_client_name')
if new_client:
    print("New client added:", new_client)
else:
    print("Failed to add new client.")
```

List clients with no file backup in the last three days:

```python
import urbackup
import time
import datetime
server = urbackup.urbackup_server("http://127.0.0.1:55414/x", "admin", "foo")
clients = server.get_status()
diff_time = 3*24*60*60 # 3 days
for client in clients:
    if client["lastbackup"]=="-" or client["lastbackup"] < time.time() - diff_time:

        if client["lastbackup"]=="-" or client["lastbackup"]==0:
            lastbackup = "Never"
        else:
            lastbackup = datetime.datetime.fromtimestamp(client["lastbackup"]).strftime("%x %X")

        print("Last file backup at {lastbackup} of client {clientname} is older than three days".format(
              lastbackup=lastbackup, clientname=client["name"] ) )
```

For more information, please refer to the [API Reference](https://python-urbackup.readthedocs.io/en/latest/api_reference/).

## Contributing 🤝

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License 📃

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
