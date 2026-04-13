import json
from unittest.mock import MagicMock, patch

import pytest

from urbackup import (
    AccessDeniedError,
    ActionProgress,
    AuthenticationError,
    BackupEntry,
    BackupType,
    ClientNotFoundError,
    ClientStatus,
    ExtraClient,
    InstallerOS,
    LogEntry,
    UsageEntry,
    urbackup_server,
)


def _mock_response(json_data, status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data
    return resp


def _login_then(action_response):
    def side_effect(url, **kwargs):
        data = kwargs.get("data", {}) or kwargs.get("params", {})
        if "a=login" in url and not data.get("username"):
            return _mock_response({"success": True, "session": "test_ses"})
        return _mock_response(action_response)
    return side_effect


@pytest.fixture
def server():
    return urbackup_server("http://127.0.0.1:55414/x", "admin", "foo")


class TestLogin:

    @patch("requests.post")
    def test_anonymous_login(self, mock_post, server):
        mock_post.return_value = _mock_response(
            {"success": True, "session": "anon_ses"}
        )
        assert server.login() is True
        assert server._session == "anon_ses"
        assert server._logged_in is True

    @patch("requests.post")
    def test_password_login_md5(self, mock_post, server):
        responses = [
            _mock_response({"success": False}),
            _mock_response({"ses": "salt_ses", "salt": "abc", "rnd": "xyz"}),
            _mock_response({"success": True}),
        ]
        mock_post.side_effect = responses
        assert server.login() is True
        assert server._logged_in is True

    @patch("requests.post")
    def test_password_login_pbkdf2(self, mock_post, server):
        responses = [
            _mock_response({"success": False}),
            _mock_response(
                {"ses": "s", "salt": "abc", "rnd": "xyz", "pbkdf2_rounds": 10000}
            ),
            _mock_response({"success": True}),
        ]
        mock_post.side_effect = responses
        assert server.login() is True

    @patch("requests.post")
    def test_login_bad_password(self, mock_post, server):
        responses = [
            _mock_response({"success": False}),
            _mock_response({"ses": "s", "salt": "abc", "rnd": "xyz"}),
            _mock_response({"success": False}),
        ]
        mock_post.side_effect = responses
        assert server.login() is False

    @patch("requests.post")
    def test_login_unknown_user(self, mock_post, server):
        responses = [
            _mock_response({"success": False}),
            _mock_response({}),
        ]
        mock_post.side_effect = responses
        assert server.login() is False

    @patch("requests.post")
    def test_already_logged_in(self, mock_post, server):
        server._logged_in = True
        assert server.login() is True
        mock_post.assert_not_called()


class TestLegacyAPI:

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1", "online": True}], "server_identity": "id123"}
    ))
    def test_get_status(self, mock_post, server):
        clients = server.get_status()
        assert len(clients) == 1
        assert clients[0]["name"] == "pc1"

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1"}], "server_identity": "id123"}
    ))
    def test_get_server_identity(self, mock_post, server):
        assert server.get_server_identity() == "id123"

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1"}]}
    ))
    def test_get_client_status(self, mock_post, server):
        client = server.get_client_status("pc1")
        assert client["id"] == 1

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1"}]}
    ))
    def test_get_client_status_not_found(self, mock_post, server):
        assert server.get_client_status("nonexistent") is None

    @patch("requests.post", side_effect=_login_then(
        {"progress": [{"clientid": 1, "id": 10, "action": 1, "pcdone": 50}]}
    ))
    def test_get_actions(self, mock_post, server):
        actions = server.get_actions()
        assert len(actions) == 1
        assert actions[0]["pcdone"] == 50

    @patch("requests.post", side_effect=_login_then(
        {"usage": [{"name": "pc1", "used": 1024}]}
    ))
    def test_get_usage(self, mock_post, server):
        usage = server.get_usage()
        assert usage[0]["used"] == 1024

    @patch("requests.post", side_effect=_login_then(
        {"logdata": [{"id": 5, "msg": "test log", "loglevel": 3, "time": 100}]}
    ))
    def test_get_livelog(self, mock_post, server):
        log = server.get_livelog()
        assert log[0]["msg"] == "test log"
        assert server._lastlogid == 5

    @patch("requests.post", side_effect=_login_then(
        {"status": [], "extra_clients": [{"id": 1, "hostname": "10.0.0.1"}]}
    ))
    def test_get_extra_clients(self, mock_post, server):
        extras = server.get_extra_clients()
        assert extras[0]["hostname"] == "10.0.0.1"

    @patch("requests.post")
    def test_start_incr_file_backup(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"result": [{"start_ok": True}]}),
        ]
        assert server.start_incr_file_backup("pc1") is True

    @patch("requests.post")
    def test_start_full_file_backup(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"result": [{"start_ok": True}]}),
        ]
        assert server.start_full_file_backup("pc1") is True

    @patch("requests.post")
    def test_start_incr_image_backup(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"result": [{"start_ok": True}]}),
        ]
        assert server.start_incr_image_backup("pc1") is True

    @patch("requests.post")
    def test_start_full_image_backup(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"result": [{"start_ok": True}]}),
        ]
        assert server.start_full_image_backup("pc1") is True

    @patch("requests.post")
    def test_stop_action(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"progress": []}),
        ]
        assert server.stop_action({"clientid": 1, "id": 10}) is True

    def test_stop_action_missing_keys(self, server):
        assert server.stop_action({}) is False

    @patch("requests.post")
    def test_add_extra_client(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": []}),
        ]
        assert server.add_extra_client("10.0.0.2") is True

    @patch("requests.post")
    def test_remove_extra_client(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": []}),
        ]
        assert server.remove_extra_client(1) is True

    @patch("requests.post")
    def test_add_client(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"new_clientid": 5, "new_authkey": "abc"}),
        ]
        result = server.add_client("new_pc")
        assert result["new_clientid"] == 5

    @patch("requests.post")
    def test_add_client_already_exists(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"already_exists": True}),
        ]
        assert server.add_client("existing_pc") is None

    @patch("requests.post")
    def test_get_global_settings(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"settings": {"backup_window": "1-7/0-24"}}),
        ]
        settings = server.get_global_settings()
        assert settings["backup_window"] == "1-7/0-24"

    @patch("requests.post")
    def test_set_global_setting(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"settings": {"backup_window": "1-7/0-24"}}),
            _mock_response({"saved_ok": True}),
        ]
        assert server.set_global_setting("backup_window", "1-5/8-17") is True

    @patch("requests.post")
    def test_change_client_setting(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"settings": {"key1": "old", "key2": "val2"}}),
            _mock_response({"saved_ok": True}),
        ]
        assert server.change_client_setting("pc1", "key1", "new") is True

    @patch("requests.post")
    def test_change_client_setting_key_not_found(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"settings": {"key1": "old"}}),
        ]
        assert server.change_client_setting("pc1", "nonexistent", "val") is False

    @patch("requests.post")
    def test_get_client_authkey(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"settings": {"internet_authkey": "secret123"}}),
        ]
        assert server.get_client_authkey("pc1") == "secret123"


class TestTypedAPI:

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1", "online": True}]}
    ))
    def test_get_client_statuses(self, mock_post, server):
        clients = server.get_client_statuses()
        assert len(clients) == 1
        assert isinstance(clients[0], ClientStatus)
        assert clients[0].name == "pc1"
        assert clients[0].id == 1

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1"}]}
    ))
    def test_get_client_status_by_name(self, mock_post, server):
        client = server.get_client_status_by_name("pc1")
        assert isinstance(client, ClientStatus)
        assert client.id == 1

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1"}]}
    ))
    def test_get_client_status_by_name_not_found(self, mock_post, server):
        with pytest.raises(ClientNotFoundError):
            server.get_client_status_by_name("nonexistent")

    @patch("requests.post", side_effect=_login_then(
        {"status": [{"id": 1, "name": "pc1"}], "server_identity": "id123"}
    ))
    def test_get_server_identity_str(self, mock_post, server):
        assert server.get_server_identity_str() == "id123"

    @patch("requests.post", side_effect=_login_then(
        {"status": [], "extra_clients": [{"id": 1, "hostname": "10.0.0.1"}]}
    ))
    def test_get_extra_clients_typed(self, mock_post, server):
        extras = server.get_extra_clients_typed()
        assert len(extras) == 1
        assert isinstance(extras[0], ExtraClient)
        assert extras[0].hostname == "10.0.0.1"

    @patch("requests.post", side_effect=_login_then(
        {"progress": [{"clientid": 1, "id": 10, "action": 1, "pcdone": 50}]}
    ))
    def test_get_actions_typed(self, mock_post, server):
        actions = server.get_actions_typed()
        assert len(actions) == 1
        assert isinstance(actions[0], ActionProgress)
        assert actions[0].progress_percent == 50

    @patch("requests.post", side_effect=_login_then(
        {"usage": [{"name": "pc1", "used": 2048, "files": 10, "images": 2}]}
    ))
    def test_get_usage_typed(self, mock_post, server):
        usage = server.get_usage_typed()
        assert isinstance(usage[0], UsageEntry)
        assert usage[0].used == 2048

    @patch("requests.post", side_effect=_login_then(
        {"logdata": [{"id": 7, "msg": "backup done", "loglevel": 3, "time": 200}]}
    ))
    def test_get_livelog_typed(self, mock_post, server):
        logs = server.get_livelog_typed()
        assert isinstance(logs[0], LogEntry)
        assert logs[0].message == "backup done"
        assert server._lastlogid == 7

    @patch("requests.post")
    def test_start_backup_typed(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"result": [{"start_ok": True}]}),
        ]
        assert server.start_backup_typed("pc1", BackupType.INCR_FILE) is True

    @patch("requests.post")
    def test_require_login_raises(self, mock_post, server):
        mock_post.return_value = _mock_response({}, status_code=500)
        with pytest.raises(AuthenticationError):
            server.get_client_statuses()

    @patch("requests.post", side_effect=_login_then(
        {"backups": [{"id": 100, "clientid": 1, "backuptime": 99999}]}
    ))
    def test_get_backups(self, mock_post, server):
        backups = server.get_backups(clientid=1)
        assert len(backups) == 1
        assert isinstance(backups[0], BackupEntry)
        assert backups[0].id == 100

    @patch("requests.post", side_effect=_login_then(
        {"settings": {"backup_window": "1-7/0-24"}}
    ))
    def test_get_global_settings_typed(self, mock_post, server):
        settings = server.get_global_settings_typed()
        assert settings["backup_window"] == "1-7/0-24"

    @patch("requests.post")
    def test_set_global_setting_typed(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"settings": {"backup_window": "1-7/0-24"}}),
            _mock_response({"saved_ok": True}),
        ]
        assert server.set_global_setting_typed("backup_window", "1-5/8-17") is True

    @patch("requests.post")
    def test_change_client_setting_typed(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"settings": {"key1": "old"}}),
            _mock_response({"saved_ok": True}),
        ]
        assert server.change_client_setting_typed("pc1", "key1", "new") is True

    @patch("requests.post")
    def test_change_client_setting_typed_key_not_found(self, mock_post, server):
        mock_post.side_effect = [
            _mock_response({"success": True, "session": "s"}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"status": [{"id": 1, "name": "pc1"}]}),
            _mock_response({"settings": {"key1": "old"}}),
        ]
        with pytest.raises(KeyError):
            server.change_client_setting_typed("pc1", "nonexistent", "val")


class TestDataclasses:

    def test_client_status_from_dict(self):
        data = {"id": 1, "name": "pc1", "online": True, "ip": "192.168.1.1"}
        cs = ClientStatus.from_dict(data)
        assert cs.id == 1
        assert cs.online is True
        assert cs.raw == data

    def test_backup_entry_from_dict(self):
        data = {"id": 10, "clientid": 1, "backuptime": 12345, "size_bytes": 999}
        be = BackupEntry.from_dict(data)
        assert be.size_bytes == 999

    def test_log_entry_from_dict(self):
        data = {"id": 1, "msg": "hello", "loglevel": 3, "time": 100}
        le = LogEntry.from_dict(data)
        assert le.message == "hello"
        assert le.level == 3

    def test_action_progress_from_dict(self):
        data = {"clientid": 1, "id": 5, "pcdone": 75, "action": 1}
        ap = ActionProgress.from_dict(data)
        assert ap.progress_percent == 75

    def test_extra_client_from_dict(self):
        data = {"id": 1, "hostname": "10.0.0.1"}
        ec = ExtraClient.from_dict(data)
        assert ec.hostname == "10.0.0.1"

    def test_usage_entry_from_dict(self):
        data = {"name": "pc1", "used": 1024, "files": 5, "images": 2}
        ue = UsageEntry.from_dict(data)
        assert ue.files == 5


class TestConstructor:

    def test_basic_auth(self):
        s = urbackup_server(
            "http://localhost/x", "admin", "pass",
            basic_username="user", basic_password="pw",
        )
        headers = s._build_headers()
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

    def test_no_basic_auth(self):
        s = urbackup_server("http://localhost/x", "admin", "pass")
        headers = s._build_headers()
        assert "Authorization" not in headers

    def test_url_trailing_slash_stripped(self):
        s = urbackup_server("http://localhost/x/", "admin", "pass")
        assert s._server_url == "http://localhost/x"
