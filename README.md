#  Python UrBackup ![Icon](https://www.urbackup.org/favicon.ico)

[![PyPI](https://img.shields.io/pypi/v/python-urbackup)](https://pypi.org/project/python-urbackup/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dirconfig)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/judahpaul16/python-urbackup/workflow.yaml)](https://github.com/judahpaul16/python-urbackup/actions)
[![Coverage Status](https://coveralls.io/repos/github/judahpaul16/python-urbackup/badge.svg?branch=master)](https://coveralls.io/github/judahpaul16/python-urbackup?branch=master)
[![Documentation Status](https://readthedocs.org/projects/python-urbackup/badge/?version=latest)](https://python-urbackup.readthedocs.io/en/latest/?badge=latest)

Python wrapper to access and control an UrBackup server.

*Originally [urbackup-server-web-api-wrapper](https://github.com/uroni/urbackup-server-python-web-api-wrapper)*

## Installation

Install with:

	pip3 install python-urbackup

## Usage



## Examples

Start a full file backup:

```python
import urbackup_api

server = urbackup_api.urbackup_server("http://127.0.0.1:55414/x", "admin", "foo")

server.start_full_file_backup("testclient0")
```

List clients with no file backup in the last three days:

```python
import urbackup_api
import time
import datetime
server = urbackup_api.urbackup_server("http://127.0.0.1:55414/x", "admin", "foo")
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

## License 📃

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.