from __future__ import annotations

import logging
from typing import Any

from ._base import _UrbackupBase
from ._types import (
    AccessDeniedError,
    ActionProgress,
    AuthenticationError,
    BackupEntry,
    BackupType,
    ClientNotFoundError,
    ClientStatus,
    ExtraClient,
    Group,
    InstallerOS,
    LogEntry,
    UsageEntry,
    User,
    UserAlreadyExistsError,
)

logger = logging.getLogger("python-urbackup")


class _TypedAPI(_UrbackupBase):

    def _require_login(self) -> None:
        if not self.login():
            raise AuthenticationError("Login failed")

    def _get_status_response(self) -> dict[str, Any]:
        self._require_login()
        status = self._get_json("status")
        if not status or "status" not in status:
            raise AccessDeniedError("Cannot access server status")
        return status

    def get_client_statuses(self) -> list[ClientStatus]:
        status = self._get_status_response()
        return [ClientStatus.from_dict(c) for c in status["status"]]

    def get_client_status_by_name(self, clientname: str) -> ClientStatus:
        status = self._get_status_response()
        for client in status["status"]:
            if client["name"] == clientname:
                return ClientStatus.from_dict(client)
        raise ClientNotFoundError(f"Client not found: {clientname}")

    def get_server_identity_str(self) -> str:
        status = self._get_status_response()
        if "server_identity" not in status:
            raise AccessDeniedError("Cannot access server identity")
        return status["server_identity"]

    def get_extra_clients_typed(self) -> list[ExtraClient]:
        status = self._get_status_response()
        return [
            ExtraClient.from_dict(ec)
            for ec in status.get("extra_clients", [])
        ]

    def get_backups(
        self,
        clientid: int,
    ) -> list[BackupEntry]:
        self._require_login()
        resp = self._get_json("backups", {"sa": "backups", "clientid": clientid})
        if not resp or "backups" not in resp:
            return []
        return [BackupEntry.from_dict(b) for b in resp["backups"]]

    def get_image_backups(
        self,
        clientid: int,
    ) -> list[BackupEntry]:
        self._require_login()
        resp = self._get_json(
            "backups",
            {"sa": "backups", "clientid": clientid},
        )
        if not resp or "image_backups" not in resp:
            return []
        return [BackupEntry.from_dict(b) for b in resp["image_backups"]]

    def start_backup_typed(
        self,
        clientname: str,
        backup_type: BackupType,
    ) -> bool:
        client = self.get_client_status_by_name(clientname)
        ret = self._get_json(
            "start_backup",
            {"start_client": client.id, "start_type": backup_type.value},
        )
        if (
            ret is None
            or "result" not in ret
            or len(ret["result"]) != 1
            or not ret["result"][0].get("start_ok")
        ):
            return False
        return True

    def get_actions_typed(self) -> list[ActionProgress]:
        self._require_login()
        ret = self._get_json("progress")
        if not ret or "progress" not in ret:
            return []
        return [ActionProgress.from_dict(a) for a in ret["progress"]]

    def stop_action_typed(self, action: ActionProgress) -> bool:
        self._require_login()
        ret = self._get_json(
            "progress",
            {"stop_clientid": action.clientid, "stop_id": action.id},
        )
        return ret is not None and "progress" in ret

    def get_usage_typed(self) -> list[UsageEntry]:
        self._require_login()
        usage = self._get_json("usage")
        if not usage or "usage" not in usage:
            return []
        return [UsageEntry.from_dict(u) for u in usage["usage"]]

    def get_livelog_typed(
        self,
        clientid: int = 0,
    ) -> list[LogEntry]:
        self._require_login()
        log = self._get_json(
            "livelog",
            {"clientid": clientid, "lastid": self._lastlogid},
        )
        if not log or "logdata" not in log:
            return []
        entries = [LogEntry.from_dict(e) for e in log["logdata"]]
        if entries:
            self._lastlogid = entries[-1].id
        return entries

    def get_global_settings_typed(self) -> dict[str, Any]:
        self._require_login()
        settings = self._get_json("settings", {"sa": "general"})
        if not settings or "settings" not in settings:
            raise AccessDeniedError("Cannot access global settings")
        return settings["settings"]

    def set_global_setting_typed(self, key: str, value: Any) -> bool:
        settings = self.get_global_settings_typed()
        settings[key] = value
        settings["sa"] = "general_save"
        ret = self._get_json("settings", settings)
        return ret is not None and "saved_ok" in ret

    def get_client_settings_typed(
        self,
        clientname: str,
    ) -> dict[str, Any]:
        client = self.get_client_status_by_name(clientname)
        settings = self._get_json(
            "settings",
            {"sa": "clientsettings", "t_clientid": client.id},
        )
        if not settings or "settings" not in settings:
            raise AccessDeniedError(
                f"Cannot access settings for client {clientname}"
            )
        return settings["settings"]

    def change_client_setting_typed(
        self,
        clientname: str,
        key: str,
        new_value: Any,
    ) -> bool:
        client = self.get_client_status_by_name(clientname)
        current_settings = self.get_client_settings_typed(clientname)

        if key not in current_settings:
            raise KeyError(f"Setting {key} not found for client {clientname}")

        current_settings[key] = new_value
        save_payload = {
            "overwrite": "true",
            "sa": "clientsettings_save",
            "t_clientid": client.id,
        }
        save_payload.update(current_settings)
        ret = self._get_json("settings", save_payload)
        return ret is not None and "saved_ok" in ret

    def get_users(self) -> list[User]:
        self._require_login()
        ret = self._get_json("settings", {"sa": "listusers"})
        if not ret or "users" not in ret:
            return []
        return [User.from_dict(u) for u in ret["users"]]

    def get_groups(self) -> list[Group]:
        self._require_login()
        ret = self._get_json("settings", {"sa": "listgroups"})
        if not ret or "groups" not in ret:
            return []
        return [Group.from_dict(g) for g in ret["groups"]]

    def add_user(
        self,
        username: str,
        password: str,
        rights: str = "all",
    ) -> bool:
        self._require_login()
        salt = self._get_json("salt", {"username": username})
        if salt and salt.get("salt"):
            raise UserAlreadyExistsError(f"User already exists: {username}")

        ret = self._get_json(
            "settings",
            {
                "sa": "updatesettings",
                "username": username,
                "password": password,
                "rights": rights,
            },
        )
        return ret is not None and ret.get("saved_ok", False)

    def download_installer_typed(
        self,
        installer_fn: str,
        new_clientname: str,
        os: InstallerOS = InstallerOS.LINUX,
    ) -> bool:
        self._require_login()
        new_client = self._get_json("add_client", {"clientname": new_clientname})
        if not new_client:
            return False

        if "already_exists" in new_client:
            client = self.get_client_status_by_name(new_clientname)
            return self._download_file(
                "download_client",
                installer_fn,
                {"clientid": client.id},
            )

        if "new_authkey" not in new_client:
            return False

        return self._download_file(
            "download_client",
            installer_fn,
            {
                "clientid": new_client["new_clientid"],
                "authkey": new_client["new_authkey"],
                "os": os.value,
            },
        )
