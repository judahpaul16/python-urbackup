import unittest
from unittest.mock import patch, MagicMock
from urbackup import urbackup_server, installer_os
import datetime
import time

class TestUrBackupServer(unittest.TestCase):
    def setUp(self):
        self.server_url = "http://127.0.0.1:55414/x"
        self.username = "admin"
        self.password = "foo"
        self.server = urbackup_server(self.server_url, self.username, self.password)

    @patch('urbackup.urbackup_server.get_extra_clients')
    @patch('urbackup.urbackup_server.remove_extra_client')
    def test_manage_extra_clients(self, mock_remove, mock_get_clients):
        # Mocking the get_extra_clients and remove_extra_client methods
        mock_get_clients.return_value = [{'id': 'client1'}, {'id': 'client2'}]
        
        # Execute the method to test
        extra_clients = self.server.get_extra_clients()
        for extra_client in extra_clients:
            self.server.remove_extra_client(extra_client["id"])

        # Assert that remove_extra_client was called for each client
        mock_remove.assert_any_call('client1')
        mock_remove.assert_any_call('client2')
        self.assertEqual(mock_remove.call_count, 2)

    @patch('urbackup.urbackup_server.add_extra_client')
    def test_add_extra_clients(self, mock_add_client):
        # Setup
        computernames = ["2.2.2.2", "3.3.3.3"]
        mock_add_client.return_value = True

        # Test
        for ip in computernames:
            result = self.server.add_extra_client(ip)
            self.assertTrue(result)
            mock_add_client.assert_called_with(ip)

    @patch('urbackup.urbackup_server.get_status')
    @patch('urbackup.urbackup_server.get_usage')
    def test_check_status_and_usage(self, mock_get_usage, mock_get_status):
        # Mocking responses
        mock_get_status.return_value = [{'name': 'client1', 'lastbackup': 1590000000}]
        mock_get_usage.return_value = [{'client': 'client1', 'data': 1000}]

        # Execution
        clients = self.server.get_status()
        usage = self.server.get_usage()

        # Verify length and data integrity
        self.assertEqual(len(clients), len(usage))
        self.assertGreater(len(clients), 0)
        self.assertEqual(clients[0]['name'], 'client1')
        self.assertEqual(usage[0]['data'], 1000)

    @patch('urbackup.urbackup_server.get_status')
    def test_backup_status_check(self, mock_get_status):
        mock_get_status.return_value = [{'name': 'client1', 'lastbackup': time.time() - (4 * 24 * 60 * 60)}]
        clients = self.server.get_status()
        for client in clients:
            if client['lastbackup'] < time.time() - (3 * 24 * 60 * 60):
                lastbackup = datetime.datetime.fromtimestamp(client['lastbackup']).strftime('%x %X')
                self.assertTrue("Last file backup at" in f"Last file backup at {lastbackup} of client {client['name']} is older than three days")

    @patch('urbackup.urbackup_server.download_installer')
    def test_download_installer(self, mock_download):
        # Setup
        mock_download.return_value = True
        result = self.server.download_installer("test.exe", "test", installer_os.Windows)
        self.assertTrue(result)
        mock_download.assert_called_with("test.exe", "test", installer_os.Windows)

if __name__ == '__main__':
    unittest.main()
