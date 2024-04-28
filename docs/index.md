# Python UrBackup [![urbackup.org](urbackup.png)](https://www.urbackup.org/)
[![PyPI](https://img.shields.io/pypi/v/python-urbackup)](https://pypi.org/project/python-urbackup/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dirconfig)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/judahpaul16/python-urbackup/workflow.yaml)](https://github.com/judahpaul16/python-urbackup/actions)
[![Coverage Status](https://coveralls.io/repos/github/judahpaul16/python-urbackup/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/judahpaul16/python-urbackup?branch=master)
[![Documentation Status](https://readthedocs.org/projects/python-urbackup/badge/?version=latest)](https://python-urbackup.readthedocs.io/en/latest/?badge=latest)

Python UrBackup is a powerful Python wrapper designed to interact with UrBackup servers. This library allows you to manage backups, restore operations, and monitor the server status programmatically.

*Originally [urbackup-server-web-api-wrapper](https://github.com/uroni/urbackup-server-python-web-api-wrapper)*

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
