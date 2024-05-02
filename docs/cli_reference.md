# CLI Reference

The UrBackup Client CLI allows you to interact with the UrBackup server from a client machine.

*Important Note: For Windows the command-line tool is `urbackupclient_cmd`, usually located at `C:\Program Files\UrBackup\UrBackupClient_cmd.exe`. Mac and Linux use `urbackupclientctl`.*

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

The Urbackup Server CLI allows you to interact with the UrBackup server from the server machine itself.

CLI options for `urbackupsrv` are as follows:

```sh
USAGE:

        urbackupsrv [--help] [--version] <command> [<args>]

Get specific command help with urbackupsrv <command> --help

        urbackupsrv run
                Run UrBackup server

        urbackupsrv verify-hashes
                Verify file backup hashes

        urbackupsrv remove-unknown
                Remove unknown files and directories from backup storage and fix symbolic links in backup storage

        urbackupsrv reset-admin-pw
                Reset web interface administrator password

        urbackupsrv cleanup
                Cleanup file/image backups from backup storage

        urbackupsrv repair-database
                Try to repair UrBackup database

        urbackupsrv defrag-database
                Rebuild UrBackup database

        urbackupsrv export-auth-log
                Export authentication log to csv file

        urbackupsrv decompress-file
                Decompress UrBackup compressed file

        urbackupsrv mount-vhd
                Mount VHD file

        urbackupsrv assemble
                Assemble VHD(Z) volumes into one disk VHD file
```

For more information, please refer to the [UrBackup Administration Documentation](https://www.urbackup.org/administration_manual.html).