# CLI Reference

The UrBackup CLI is a command-line interface that allows you to interact with the UrBackup server from a client machine.

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

For more information, please refer to the [UrBackup Administration Documentation](https://www.urbackup.org/administration_manual.html).