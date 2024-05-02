# API Reference 

This section provides detailed documentation for all functions and classes available in the Python UrBackup API.

## Classes

### `installer_os`

An enumeration of supported operating systems for installers.

- `Windows`: Represents a Windows operating system.
- `Linux`: Represents a Linux operating system.

### `Server`

This class provides methods to interact with the UrBackup server.

#### Attributes

- `server_basic_username`: Username for basic authentication.
- `server_basic_password`: Password for basic authentication.
- `action_incr_file`: Constant for incremental file backup action.
- `action_full_file`: Constant for full file backup action.
- `action_incr_image`: Constant for incremental image backup action.
- `action_full_image`: Constant for full image backup action.
- `action_resumed_incr_file`: Constant for resumed incremental file backup action.
- `action_resumed_full_file`: Constant for resumed full file backup action.
- `action_file_restore`: Constant for file restore action.
- `action_image_restore`: Constant for image restore action.
- `action_client_update`: Constant for client update action.
- `action_check_db_integrity`: Constant for database integrity check action.
- `action_backup_db`: Constant for database backup action.
- `action_recalc_stats`: Constant for recalculating statistics action.

#### Methods

- `__init__(url, username, password)`: Initializes a new `Server` instance.
- `login()`: Logs in to the UrBackup server and returns `True` on success.
- `get_client_status(client_name)`: Retrieves the status of a specified client.
- `download_installer(installer_fn, new_clientname, os='linux')`: Downloads the installer for a specified client and operating system.
- `add_client(clientname)`: Adds a new client to the server.
- `get_global_settings()`: Retrieves global settings from the server.
- `set_global_setting(key, new_value)`: Sets a global setting on the server.
- `get_client_settings(clientname)`: Retrieves settings for a specified client.
- `change_client_setting(clientname, key, new_value)`: Changes a setting for a specified client.
- `get_client_authkey(clientname)`: Retrieves the authentication key for a specified client.
- `get_server_identity()`: Retrieves the server's identity.
- `get_status()`: Retrieves the overall status of the server.
- `get_livelog(clientid=0)`: Retrieves live log entries for a specified client.
- `get_usage()`: Retrieves usage statistics from the server.
- `get_extra_clients()`: Retrieves a list of extra clients added to the server.
- `start_incr_file_backup(clientname)`: Starts an incremental file backup for a specified client.
- `start_full_file_backup(clientname)`: Starts a full file backup for a specified client.
- `start_incr_image_backup(clientname)`: Starts an incremental image backup for a specified client.
- `start_full_image_backup(clientname)`: Starts a full image backup for a specified client.
- `get_client_backups(clientid)`: Retrieves a list of backups for a specified client.
- `get_backup_content(clientid, backupid, path="/")`: Retrieves the content of a backup for a specified client.
- `download_backup_file(clientid, backupid, path)`: Downloads a file from a backup for a specified client.
- `get_groups()`: Retrieves a list of groups from the server.
- `get_clients_with_group(groupid)`: Retrieves a list of clients in a specified group.
- `add_extra_client(addr)`: Adds an extra client by hostname.
- `remove_extra_client(ecid)`: Removes an extra client by ID.
- `get_actions()`: Retrieves current actions being performed on the server.
- `stop_action(action)`: Stops a specific action on the server.

#### Private Methods

- `_get_response(action, params, method='POST')`: Sends a request to the server and retrieves the response.
- `_get_json(action, params={})`: Sends a JSON request to the server and parses the response.
- `_download_file(action, outputfn, params)`: Downloads a file from the server based on specified parameters.
- `_md5(s)`: Calculates the MD5 hash of a given string.

Please refer to the source code for more detailed information on each method, including parameters and expected response types.

For more specific information regarding urbackup administration, please refer to the [official UrBackup documentation](https://www.urbackup.org/administration_manual.html).