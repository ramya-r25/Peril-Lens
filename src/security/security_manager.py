from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class ThreatLensSecurity:
    """
    Security services for the offline ThreatLens application.

    Provides:
    - Local administrator authentication
    - scrypt password hashing
    - AES-256-GCM encryption
    - Encrypted audit logging
    - Password-derived encryption keys
    - No hard-coded encryption keys
    """

    AUTH_VERSION = 1
    ENCRYPTION_VERSION = b"TLENC1"
    ASSOCIATED_DATA = b"ThreatLens-v1"

    def __init__(self, root: Path):
        self.root = Path(root)

        self.security_dir = self.root / "security"
        self.security_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.auth_file = self.security_dir / "auth.json"
        self.audit_file = self.security_dir / "audit.enc"

    # ============================================================
    # PASSWORD HASHING
    # ============================================================

    @staticmethod
    def _derive_password_hash(
        password: str,
        salt: bytes
    ) -> bytes:
        """
        Derive a password hash using scrypt.
        """

        return hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
            dklen=32,
        )

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    def is_configured(self) -> bool:
        """
        Check whether the local administrator account exists.
        """

        return self.auth_file.exists()

    def create_admin(self, password: str) -> None:
        """
        Create the initial local administrator credential.

        Only a salted scrypt hash is stored.
        The plaintext password is never written to disk.
        """

        if len(password) < 10:
            raise ValueError(
                "Password must contain at least 10 characters."
            )

        salt = secrets.token_bytes(16)

        password_hash = self._derive_password_hash(
            password,
            salt
        )

        payload = {
            "version": self.AUTH_VERSION,
            "algorithm": "scrypt",
            "salt": base64.b64encode(
                salt
            ).decode("ascii"),
            "password_hash": base64.b64encode(
                password_hash
            ).decode("ascii"),
            "created_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        self.auth_file.write_text(
            json.dumps(
                payload,
                indent=2
            ),
            encoding="utf-8"
        )

    def verify_password(
        self,
        password: str
    ) -> bool:
        """
        Verify a password against the stored scrypt hash.
        """

        if not self.auth_file.exists():
            return False

        try:
            payload = json.loads(
                self.auth_file.read_text(
                    encoding="utf-8"
                )
            )

            salt = base64.b64decode(
                payload["salt"]
            )

            expected = base64.b64decode(
                payload["password_hash"]
            )

            actual = self._derive_password_hash(
                password,
                salt
            )

            return hmac.compare_digest(
                actual,
                expected
            )

        except Exception:
            return False

    # ============================================================
    # ENCRYPTION KEY DERIVATION
    # ============================================================

    def derive_encryption_key(
        self,
        password: str
    ) -> bytes:
        """
        Derive a 256-bit AES key from the authenticated password.
        """

        if not self.auth_file.exists():
            raise RuntimeError(
                "ThreatLens authentication is not configured."
            )

        payload = json.loads(
            self.auth_file.read_text(
                encoding="utf-8"
            )
        )

        base_salt = base64.b64decode(
            payload["salt"]
        )

        encryption_salt = hashlib.sha256(
            b"ThreatLens-AES-256-GCM-v1"
            + base_salt
        ).digest()[:16]

        return hashlib.scrypt(
            password.encode("utf-8"),
            salt=encryption_salt,
            n=2**14,
            r=8,
            p=1,
            dklen=32,
        )

    # ============================================================
    # AES-256-GCM ENCRYPTION
    # ============================================================

    @classmethod
    def encrypt_bytes(
        cls,
        data: bytes,
        key: bytes
    ) -> bytes:
        """
        Encrypt bytes using AES-256-GCM.

        Format:

        TLENC1
        + 12-byte nonce
        + authenticated ciphertext
        """

        if len(key) != 32:
            raise ValueError(
                "AES-256 requires a 32-byte key."
            )

        nonce = secrets.token_bytes(12)

        cipher = AESGCM(key)

        ciphertext = cipher.encrypt(
            nonce,
            data,
            cls.ASSOCIATED_DATA
        )

        return (
            cls.ENCRYPTION_VERSION
            + nonce
            + ciphertext
        )

    @classmethod
    def decrypt_bytes(
        cls,
        blob: bytes,
        key: bytes
    ) -> bytes:
        """
        Decrypt and authenticate AES-256-GCM data.
        """

        if not blob.startswith(
            cls.ENCRYPTION_VERSION
        ):
            raise ValueError(
                "Unsupported ThreatLens encrypted file format."
            )

        if len(key) != 32:
            raise ValueError(
                "AES-256 requires a 32-byte key."
            )

        nonce = blob[6:18]
        ciphertext = blob[18:]

        cipher = AESGCM(key)

        return cipher.decrypt(
            nonce,
            ciphertext,
            cls.ASSOCIATED_DATA
        )

    # ============================================================
    # FILE ENCRYPTION
    # ============================================================

    def encrypt_file(
        self,
        source: Path,
        destination: Path,
        key: bytes
    ) -> None:
        """
        Encrypt a local file.
        """

        source = Path(source)
        destination = Path(destination)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        encrypted = self.encrypt_bytes(
            source.read_bytes(),
            key
        )

        destination.write_bytes(
            encrypted
        )

    def decrypt_file(
        self,
        source: Path,
        destination: Path,
        key: bytes
    ) -> None:
        """
        Decrypt a ThreatLens protected file.
        """

        source = Path(source)
        destination = Path(destination)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        decrypted = self.decrypt_bytes(
            source.read_bytes(),
            key
        )

        destination.write_bytes(
            decrypted
        )

    # ============================================================
    # ENCRYPTED AUDIT LOG
    # ============================================================

    def append_audit(
        self,
        key: bytes,
        username: str,
        action: str,
        **details: Any
    ) -> None:
        """
        Add an authenticated audit event.

        The complete audit history is stored encrypted.
        """

        event = {
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),

            "username": username,

            "action": action,

            "details": details,
        }

        existing: list[dict[str, Any]] = []

        if self.audit_file.exists():

            try:

                decrypted = self.decrypt_bytes(
                    self.audit_file.read_bytes(),
                    key
                )

                existing = json.loads(
                    decrypted.decode("utf-8")
                )

            except Exception as exc:

                raise RuntimeError(
                    "Audit log could not be authenticated "
                    "or decrypted."
                ) from exc

        existing.append(event)

        payload = json.dumps(
            existing,
            indent=2,
            ensure_ascii=False
        ).encode("utf-8")

        encrypted = self.encrypt_bytes(
            payload,
            key
        )

        self.audit_file.write_bytes(
            encrypted
        )

    def read_audit(
        self,
        key: bytes
    ) -> list[dict[str, Any]]:
        """
        Read the encrypted audit history.
        """

        if not self.audit_file.exists():
            return []

        decrypted = self.decrypt_bytes(
            self.audit_file.read_bytes(),
            key
        )

        return json.loads(
            decrypted.decode("utf-8")
        )