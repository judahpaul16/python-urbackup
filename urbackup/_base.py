from __future__ import annotations

import binascii
import hashlib
import logging
import urllib.parse
from base64 import b64encode
from typing import Any

import requests

from ._types import ActionType

logger = logging.getLogger("python-urbackup")


class _UrbackupBase:

    action_incr_file = ActionType.INCR_FILE
    action_full_file = ActionType.FULL_FILE
    action_incr_image = ActionType.INCR_IMAGE
    action_full_image = ActionType.FULL_IMAGE
    action_resumed_incr_file = ActionType.RESUMED_INCR_FILE
    action_resumed_full_file = ActionType.RESUMED_FULL_FILE
    action_file_restore = ActionType.FILE_RESTORE
    action_image_restore = ActionType.IMAGE_RESTORE
    action_client_update = ActionType.CLIENT_UPDATE
    action_check_db_integrity = ActionType.CHECK_DB_INTEGRITY
    action_backup_db = ActionType.BACKUP_DB
    action_recalc_stats = ActionType.RECALC_STATS

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        *,
        basic_username: str = "",
        basic_password: str = "",
    ):
        self._server_url = url.rstrip("/")
        self._server_username = username
        self._server_password = password
        self.server_basic_username = basic_username
        self.server_basic_password = basic_password
        self._session = ""
        self._logged_in = False
        self._lastlogid = 0

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if self.server_basic_username:
            credentials = b64encode(
                f"{self.server_basic_username}:{self.server_basic_password}".encode()
            ).decode("ascii")
            headers["Authorization"] = f"Basic {credentials}"
        return headers

    def _request(
        self,
        action: str,
        params: dict[str, Any] | None = None,
        method: str = "POST",
    ) -> requests.Response:
        action_url = (
            f"{self._server_url}?{urllib.parse.urlencode({'a': action})}"
        )
        params = dict(params) if params else {}

        if self._session:
            params["ses"] = self._session

        headers = self._build_headers()

        if method == "POST":
            return requests.post(action_url, data=params, headers=headers)
        if method == "GET":
            return requests.get(action_url, params=params, headers=headers)
        raise ValueError(f"Unsupported HTTP method: {method}")

    def _get_json(
        self,
        action: str,
        params: dict[str, Any] | None = None,
        retries: int = 50,
    ) -> dict[str, Any] | None:
        for attempt in range(retries):
            response = self._request(action, params)
            if response.status_code == 200:
                return response.json()
            logger.error(
                "API call to %s failed (HTTP %d), attempt %d/%d",
                action,
                response.status_code,
                attempt + 1,
                retries,
            )
        return None

    def _download_file(
        self,
        action: str,
        output_path: str,
        params: dict[str, Any],
    ) -> bool:
        response = self._request(action, params, method="GET")
        if response.status_code != 200:
            return False
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True

    @staticmethod
    def _md5(s: str) -> str:
        return hashlib.md5(s.encode()).hexdigest()

    def _hash_password(self, salt_response: dict[str, Any]) -> str:
        salt = salt_response["salt"]
        password_md5_bin = hashlib.md5(
            (salt + self._server_password).encode()
        ).digest()
        password_hash = binascii.hexlify(password_md5_bin).decode()

        pbkdf2_rounds = int(salt_response.get("pbkdf2_rounds", 0))
        if pbkdf2_rounds > 0:
            password_hash = binascii.hexlify(
                hashlib.pbkdf2_hmac(
                    "sha256",
                    password_md5_bin,
                    salt.encode(),
                    pbkdf2_rounds,
                )
            ).decode()

        return self._md5(salt_response["rnd"] + password_hash)

    def login(self) -> bool:
        if self._logged_in:
            return True

        logger.debug("Trying anonymous login...")
        login_resp = self._get_json("login", {})

        if login_resp and login_resp.get("success"):
            self._logged_in = True
            self._session = login_resp["session"]
            return True

        logger.debug("Logging in as %s...", self._server_username)
        salt = self._get_json("salt", {"username": self._server_username})

        if not salt or "ses" not in salt:
            logger.warning("Username %s not found", self._server_username)
            return False

        self._session = salt["ses"]

        if "salt" not in salt:
            return False

        password_hash = self._hash_password(salt)

        login_resp = self._get_json(
            "login",
            {"username": self._server_username, "password": password_hash},
        )

        if not login_resp or not login_resp.get("success"):
            logger.warning("Login failed for %s", self._server_username)
            return False

        self._logged_in = True
        return True
