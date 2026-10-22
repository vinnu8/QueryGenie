from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from services import auth


class AuthServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "accounts.sqlite3"
        self.database_patch = patch.object(auth, "DATABASE_PATH", self.database_path)
        self.database_patch.start()

    def tearDown(self) -> None:
        self.database_patch.stop()
        self.temp_directory.cleanup()

    def test_account_registration_and_sign_in(self) -> None:
        user = auth.create_account("  Jane   Doe ", "Jane@Example.com", "safe-password-123")

        self.assertEqual(user["name"], "Jane Doe")
        self.assertEqual(user["email"], "jane@example.com")
        self.assertNotIn("password_hash", user)
        self.assertEqual(
            auth.authenticate("JANE@example.com", "safe-password-123"),
            user,
        )

    def test_sign_in_rejects_unknown_email_and_wrong_password(self) -> None:
        auth.create_account("Jane Doe", "jane@example.com", "safe-password-123")

        self.assertIsNone(auth.authenticate("unknown@example.com", "safe-password-123"))
        self.assertIsNone(auth.authenticate("jane@example.com", "wrong-password"))

    def test_registration_rejects_short_password_and_duplicate_email(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 10"):
            auth.create_account("Jane Doe", "jane@example.com", "short")
        auth.create_account("Jane Doe", "jane@example.com", "safe-password-123")
        with self.assertRaisesRegex(ValueError, "already exists"):
            auth.create_account("Another Name", "JANE@example.com", "safe-password-123")


if __name__ == "__main__":
    unittest.main()
