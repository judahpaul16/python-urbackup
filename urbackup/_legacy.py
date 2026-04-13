from __future__ import annotations

import logging
from typing import Any

from ._base import _UrbackupBase

logger = logging.getLogger("python-urbackup")


class _LegacyAPI(_UrbackupBase):

    def get_client_status(self, clientname: str) -> dict[str, Any] | None:
        if not self.login():
            return None

        status = self._get_json("status")
        if not status or "status" not in status:
            return None

        for client in status["status"]:
            if client["name"] == clientname:
                return client

        logger.warning("Could not find client %s", clientname)
        return None

    def download_installer(
        self,
        installer_fn: str,
        new_clientname: str,
        os: str = "linux",
    ) -> bool:
        if os.lower() not in ("linux", "osx", "mac", "windows"):
            raise ValueError(f"Unsupported OS: {os}")

        if not self.login():
            return False

        new_client = self._get_json("add_client", {"clientname": new_clientname})
        if not new_client:
            return False

        if "already_exists" in new_client:
            status = self.get_client_status(new_clientname)
            if status is None:
                return False
            return self._download_file(
                "download_client",
                installer_fn,
                {"clientid": status["id"]},
            )

        if "new_authkey" not in new_client:
            return False

        return self._download_file(
            "download_client",
            installer_fn,
            {
                "clientid": new_client["new_clientid"],
                "authkey": new_client["new_authkey"],
                "os": os,
            },
        )

    def add_client(self, clientname: str) -> dict[str, Any] | None:
        if not self.login():
            return None
        ret = self._get_json("add_client", {"clientname": clientname})
        if ret is None or "already_exists" in ret:
            return None
        return ret

    def get_global_settings(self) -> dict[str, Any] | None:
        if not self.login():
            return None
        settings = self._get_json("settings", {"sa": "general"})
        if not settings or "settings" not in settings:
            return None
        return settings["settings"]

    def set_global_setting(
        self,
        key: str,
        new_value: Any,
    ) -> bool:
        if not self.login():
            return False
        settings = self._get_json("settings", {"sa": "general"})
        if not settings or "settings" not in settings:
            return False
        settings["settings"][key] = new_value
        settings["settings"]["sa"] = "general_save"
        ret = self._get_json("settings", settings["settings"])
        return ret is not None and "saved_ok" in ret

    def get_client_settings(
        self,
        clientname: str,
    ) -> dict[str, Any] | None:
        if not self.login():
            return None
        client = self.get_client_status(clientname)
        if client is None:
            return None
        settings = self._get_json(
            "settings",
            {"sa": "clientsettings", "t_clientid": client["id"]},
        )
        if not settings or "settings" not in settings:
            return None
        return settings["settings"]

    def change_client_setting(
        self,
        clientname: str,
        key: str,
        new_value: Any,
    ) -> bool:
        if not self.login():
            return False
        client = self.get_client_status(clientname)
        if client is None:
            return False

        current_settings = self.get_client_settings(clientname)
        if current_settings is None:
            return False

        if key not in current_settings:
            logger.warning("Setting key %s not found for client %s", key, clientname)
            return False

        current_settings[key] = new_value
        save_payload = {
            "overwrite": "true",
            "sa": "clientsettings_save",
            "t_clientid": client["id"],
        }
        save_payload.update(current_settings)
        ret = self._get_json("settings", save_payload)
        return ret is not None and "saved_ok" in ret

    def get_client_authkey(self, clientname: str) -> str | None:
        if not self.login():
            return None
        settings = self.get_client_settings(clientname)
        if settings:
            return settings.get("internet_authkey")
        return None

    def get_server_identity(self) -> str | None:
        if not self.login():
            return None
        status = self._get_json("status")
        if not status or "server_identity" not in status:
            return None
        return status["server_identity"]

    def get_status(self) -> list[dict[str, Any]] | None:
        if not self.login():
            return None
        status = self._get_json("status")
        if not status or "status" not in status:
            return None
        return status["status"]

    def get_livelog(
        self,
        clientid: int = 0,
    ) -> list[dict[str, Any]] | None:
        if not self.login():
            return None
        log = self._get_json(
            "livelog",
            {"clientid": clientid, "lastid": self._lastlogid},
        )
        if not log or "logdata" not in log:
            return None
        self._lastlogid = log["logdata"][-1]["id"]
        return log["logdata"]

    def get_usage(self) -> list[dict[str, Any]] | None:
        if not self.login():
            return None
        usage = self._get_json("usage")
        if not usage or "usage" not in usage:
            return None
        return usage["usage"]

    def get_extra_clients(self) -> list[dict[str, Any]] | None:
        if not self.login():
            return None
        status = self._get_json("status")
        if not status or "extra_clients" not in status:
            return None
        return status["extra_clients"]

    def _start_backup(self, clientname: str, backup_type: str) -> bool:
        client_info = self.get_client_status(clientname)
        if not client_info:
            return False
        ret = self._get_json(
            "start_backup",
            {"start_client": client_info["id"], "start_type": backup_type},
        )
        if (
            ret is None
            or "result" not in ret
            or len(ret["result"]) != 1
            or not ret["result"][0].get("start_ok")
        ):
            return False
        return True

    def start_incr_file_backup(self, clientname: str) -> bool:
        return self._start_backup(clientname, "incr_file")

    def start_full_file_backup(self, clientname: str) -> bool:
        return self._start_backup(clientname, "full_file")

    def start_incr_image_backup(self, clientname: str) -> bool:
        return self._start_backup(clientname, "incr_image")

    def start_full_image_backup(self, clientname: str) -> bool:
        return self._start_backup(clientname, "full_image")

    def add_extra_client(self, addr: str) -> bool:
        if not self.login():
            return False
        ret = self._get_json("status", {"hostname": addr})
        return ret is not None

    def remove_extra_client(self, ecid: int) -> bool:
        if not self.login():
            return False
        ret = self._get_json("status", {"hostname": ecid, "remove": "true"})
        return ret is not None

    def get_actions(self) -> list[dict[str, Any]] | None:
        if not self.login():
            return None
        ret = self._get_json("progress")
        if not ret or "progress" not in ret:
            return None
        return ret["progress"]

    def stop_action(self, action: dict[str, Any]) -> bool:
        if "clientid" not in action or "id" not in action:
            return False
        if not self.login():
            return False
        ret = self._get_json(
            "progress",
            {"stop_clientid": action["clientid"], "stop_id": action["id"]},
        )
        return ret is not None and "progress" in ret
