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
```bash
pip install python-urbackup
```

## Usage

### Initialization

Create an instance of the `urbackup_server` by specifying the server URL, username, and password. Replace `'your_server_url'`, `'your_username'`, and `'your_password'` with your server details:

```python
from urbackup import urbackup_server

server = urbackup_server('your_server_url', 'your_username', 'your_password')
```

### Logging In

To perform any operations, you need to log in:

```python
if server.login():
    print("Login successful!")
else:
    print("Login failed!")
```

### Getting Client Status

Retrieve the status of a specific client:

```python
client_status = server.get_client_status('client_name')
if client_status:
    print(f"Client status: {client_status}")
else:
    print("Client not found or access denied.")
```

### Downloading an Installer

To download an installer for a new client, specify the file path and the client's name:

```python
if server.download_installer('path/to/installer', 'new_client_name'):
    print("Installer downloaded successfully.")
else:
    print("Failed to download installer.")
```

### Starting Backups

You can start different types of backups for a client. Here are examples of starting an incremental file backup and a full file backup:

```python
if server.start_incr_file_backup('client_name'):
    print("Incremental file backup started successfully.")
else:
    print("Failed to start incremental file backup.")

if server.start_full_file_backup('client_name'):
    print("Full file backup started successfully.")
else:
    print("Failed to start full file backup.")
```

### Managing Clients

Add a new client to the server:

```python
new_client = server.add_client('new_client_name')
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

## UrBackup CLI <img src="data:image/svg+xml,<svg fill='%234D4D4D' role='img' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><title>Windows Terminal</title><path d='M8.165 6V3h7.665v3H8.165zm-.5-3H1c-.55 0-1 .45-1 1v2h7.665V3zM23 3h-6.67v3H24V4c0-.55-.45-1-1-1zM0 6.5h24V20c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V6.5zM11.5 18c0 .3.2.5.5.5h8c.3 0 .5-.2.5-.5v-1.5c0-.3-.2-.5-.5-.5h-8c-.3 0-.5.2-.5.5V18zm-5.2-4.55l-3.1 3.1c-.25.25-.25.6 0 .8l.9.9c.25.25.6.25.8 0l4.4-4.4a.52.52 0 0 0 0-.8l-4.4-4.4c-.2-.2-.6-.2-.8 0l-.9.9c-.25.2-.25.55 0 .8l3.1 3.1z'/></svg>" width=20>

The UrBackup CLI is a command-line interface that allows you to interact with the UrBackup server from a client machine.

*Important Note: For Windows the command-line tool is `urbackupclient_cmd`. Mac and Linux use `urbackupclientctl`.*

CLI options for `urbackupclientctl` and `urbackupclientctl` are as follows:

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

## Contributing 🤝

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License 📃

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
