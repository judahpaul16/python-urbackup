import unittest
from unittest.mock import patch, MagicMock
from urbackup import Server, installer_os
import datetime
import time

class TestUrBackupServer(unittest.TestCase):
    def setUp(self):
        self.server_url = "http://127.0.0.1:55414/x"
        self.username = "admin"
        self.password = "foo"
        self.server = Server(self.server_url, self.username, self.password)

    @patch('urbackup.Server.get_server_identity')
    def test_get_server_identity(self, mock_get_server_identity):
        mock_get_server_identity.return_value = {'id': 'server1', 'name': 'TestServer'}
        server_identity = self.server.get_server_identity()
        self.assertEqual(server_identity, {'id': 'server1', 'name': 'TestServer'})

    @patch('urbackup.Server.start_incr_file_backup')
    def test_start_incr_file_backup(self, mock_start_backup):
        mock_start_backup.return_value = True
        result = self.server.start_incr_file_backup('client1')
        self.assertTrue(result)
        mock_start_backup.assert_called_with('client1')

    @patch('urbackup.Server.start_full_file_backup')
    def test_start_full_file_backup(self, mock_start_backup):
        mock_start_backup.return_value = True
        result = self.server.start_full_file_backup('client1')
        self.assertTrue(result)
        mock_start_backup.assert_called_with('client1')

    @patch('urbackup.Server.start_incr_image_backup')
    def test_start_incr_image_backup(self, mock_start_backup):
        mock_start_backup.return_value = True
        result = self.server.start_incr_image_backup('client1')
        self.assertTrue(result)
        mock_start_backup.assert_called_with('client1')

    @patch('urbackup.Server.start_full_image_backup')
    def test_start_full_image_backup(self, mock_start_backup):
        mock_start_backup.return_value = True
        result = self.server.start_full_image_backup('client1')
        self.assertTrue(result)
        mock_start_backup.assert_called_with('client1')

    @patch('urbackup.Server.get_actions')
    def test_get_actions(self, mock_get_actions):
        mock_get_actions.return_value = [{'id': 1, 'type': 'backup', 'status': 'running'}]
        actions = self.server.get_actions()
        self.assertEqual(actions, [{'id': 1, 'type': 'backup', 'status': 'running'}])

    @patch('urbackup.Server.stop_action')
    def test_stop_action(self, mock_stop_action):
        action = {'clientid': 'client1', 'id': 1}
        mock_stop_action.return_value = True
        result = self.server.stop_action(action)
        self.assertTrue(result)
        mock_stop_action.assert_called_with(action)

    @patch('urbackup.Server.login')
    @patch('urbackup.Server.get_client_status')
    @patch('urbackup.Server.get_client_settings')
    @patch('urbackup.Server._get_json')
    def test_change_client_setting(self, mock_get_json, mock_get_client_settings, mock_get_client_status, mock_login):
        mock_login.return_value = True
        mock_get_client_status.return_value = {'id': 'client1', 'name': 'TestClient'}
        mock_get_client_settings.return_value = {'key1': 'value1', 'key2': 'value2'}
        mock_get_json.return_value = {'saved_ok': True}
        result = self.server.change_client_setting('TestClient', 'key1', 'new_value')
        mock_login.assert_called_once()
        self.assertTrue(result)
        mock_get_json.assert_called_with('settings', {'key1': 'new_value', 'key2': 'value2', 'overwrite': 'true', 'sa': 'clientsettings_save', 't_clientid': 'client1'})

    @patch('urbackup.Server.get_extra_clients')
    @patch('urbackup.Server.remove_extra_client')
    def test_manage_extra_clients(self, mock_remove, mock_get_clients):
        mock_get_clients.return_value = [{'id': 'client1'}, {'id': 'client2'}]
        extra_clients = self.server.get_extra_clients()
        for extra_client in extra_clients:
            self.server.remove_extra_client(extra_client["id"])
        mock_remove.assert_any_call('client1')
        mock_remove.assert_any_call('client2')
        self.assertEqual(mock_remove.call_count, 2)

    @patch('urbackup.Server.add_extra_client')
    def test_add_extra_clients(self, mock_add_client):
        computernames = ["2.2.2.2", "3.3.3.3"]
        mock_add_client.return_value = True
        for ip in computernames:
            result = self.server.add_extra_client(ip)
            self.assertTrue(result)
            mock_add_client.assert_called_with(ip)

    @patch('urbackup.Server.get_status')
    @patch('urbackup.Server.get_usage')
    def test_check_status_and_usage(self, mock_get_usage, mock_get_status):
        mock_get_status.return_value = [{'name': 'client1', 'lastbackup': 1590000000}]
        mock_get_usage.return_value = [{'client': 'client1', 'data': 1000}]
        clients = self.server.get_status()
        usage = self.server.get_usage()
        self.assertEqual(len(clients), len(usage))
        self.assertGreater(len(clients), 0)
        self.assertEqual(clients[0]['name'], 'client1')
        self.assertEqual(usage[0]['data'], 1000)

    @patch('urbackup.Server.get_status')
    def test_backup_status_check(self, mock_get_status):
        mock_get_status.return_value = [{'name': 'client1', 'lastbackup': time.time() - (4 * 24 * 60 * 60)}]
        clients = self.server.get_status()
        for client in clients:
            if client['lastbackup'] < time.time() - (3 * 24 * 60 * 60):
                lastbackup = datetime.datetime.fromtimestamp(client['lastbackup']).strftime('%x %X')
                self.assertTrue("Last file backup at" in f"Last file backup at {lastbackup} of client {client['name']} is older than three days")

    @patch('urbackup.Server.download_installer')
    def test_download_installer(self, mock_download):
        mock_download.return_value = True
        result = self.server.download_installer("test.exe", "test", installer_os.Windows)
        self.assertTrue(result)
        mock_download.assert_called_with("test.exe", "test", installer_os.Windows)

if __name__ == '__main__':
    unittest.main()
