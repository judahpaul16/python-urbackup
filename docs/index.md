# Python UrBackup [![urbackup.org](urbackup.png)](https://www.urbackup.org/)
[![PyPI](https://img.shields.io/pypi/v/python-urbackup)](https://pypi.org/project/python-urbackup/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-urbackup)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/judahpaul16/python-urbackup/workflow.yaml)](https://github.com/judahpaul16/python-urbackup/actions)
[![Coverage Status](https://coveralls.io/repos/github/judahpaul16/python-urbackup/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/judahpaul16/python-urbackup?branch=master)
[![Documentation Status](https://readthedocs.org/projects/python-urbackup/badge/?version=latest)](https://python-urbackup.readthedocs.io/en/latest/?badge=latest)

Python wrapper to interact with UrBackup servers. Manage backups, restore operations, and monitor server status programmatically.

*Originally [urbackup-server-web-api-wrapper](https://github.com/uroni/urbackup-server-python-web-api-wrapper)*

## Features

- Legacy dict-returning API for backward compatibility
- Typed dataclass-returning API with full type hints
- Structured exception hierarchy for error handling
- MD5 and PBKDF2 authentication support
- HTTP basic auth (htpasswd) support

## Installation

```bash
pip install python-urbackup
```

Requires Python 3.10 or later.

For more detailed setup, see the [Getting Started](getting_started.md) section.

## Quick Start

```python
from urbackup import urbackup_server

server = urbackup_server("http://127.0.0.1:55414/x", "admin", "password")
if server.login():
    print("Connected!")
```

For usage examples, visit the [Usage](usage/initialization.md) section. For the full method listing, see the [API Reference](api_reference.md).
