
from utils.hash import get_password_hash, verify_password


class TestPasswordHashing:
    """Test suite for password hashing utilities."""

    def test_get_password_hash_returns_string(self):
        """Test that get_password_hash returns a string."""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)

    def test_get_password_hash_non_empty(self):
        """Test that get_password_hash returns non-empty string."""
        password = "password"
        hashed = get_password_hash(password)

        assert len(hashed) > 0

    def test_get_password_hash_different_from_original(self):
        """Test that hashed password is different from original."""
        password = "original_password"
        hashed = get_password_hash(password)

        assert hashed != password

    def test_get_password_hash_consistent_format(self):
        """Test that hashed passwords have consistent format (argon2)."""
        password = "test"
        hashed = get_password_hash(password)

        # argon2 hashes start with $argon2
        assert hashed.startswith("$argon2")

    def test_verify_password_with_correct_password(self):
        """Test verify_password returns True for correct password."""
        password = "correct_password"
        hashed = get_password_hash(password)

        assert verify_password(plain_password=password, hashed_password=hashed) is True

    def test_verify_password_with_incorrect_password(self):
        """Test verify_password returns False for incorrect password."""
        correct_password = "correct"
        wrong_password = "wrong"
        hashed = get_password_hash(correct_password)

        assert verify_password(plain_password=wrong_password, hashed_password=hashed) is False

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive."""
        password = "TestPassword123"
        hashed = get_password_hash(password)

        assert verify_password(plain_password="testpassword123", hashed_password=hashed) is False

    def test_multiple_hashes_are_different(self):
        """Test that hashing the same password multiple times produces different hashes."""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Due to salt, even same password produces different hashes
        assert hash1 != hash2

    def test_hashed_password_long_enough(self):
        """Test that hashed password is sufficiently long."""
        password = "test"
        hashed = get_password_hash(password)

        # argon2 hashes are typically 100+ characters
        assert len(hashed) > 50

    def test_get_password_hash_with_empty_password(self):
        """Test hashing empty password."""
        password = ""
        hashed = get_password_hash(password)

        assert len(hashed) > 0
        assert hashed.startswith("$argon2")

    def test_get_password_hash_with_special_characters(self):
        """Test hashing password with special characters."""
        passwords = [
            "p@ssw0rd!",
            "пароль",  # Cyrillic
            "密码",  # Chinese
            "سلمة",  # Arabic
            "pass word",  # With space
            "pass\nword",  # With newline
        ]

        for password in passwords:
            hashed = get_password_hash(password)
            assert len(hashed) > 0
            assert verify_password(plain_password=password, hashed_password=hashed) is True

    def test_verify_password_with_long_password(self):
        """Test verifying very long password."""
        password = "A" * 1000
        hashed = get_password_hash(password)

        assert verify_password(plain_password=password, hashed_password=hashed) is True
        assert verify_password(plain_password="A" * 999, hashed_password=hashed) is False

    def test_password_hash_integration(self):
        """Test full password hash and verify cycle."""
        test_passwords = [
            "simple",
            "WithMixedCase123",
            "special!@#$%chars",
            "very_long_password_" * 5
        ]

        for password in test_passwords:
            hashed = get_password_hash(password)

            # Correct password should verify
            assert verify_password(plain_password=password, hashed_password=hashed) is True

            # Incorrect password should not verify
            assert verify_password(plain_password=password + "extra", hashed_password=hashed) is False

    def test_get_password_hash_not_reversible(self):
        """Test that password hashes cannot be reversed."""
        password = "secret_password"
        hashed = get_password_hash(password)

        # Hash should not contain original password
        assert password not in hashed

    def test_verify_password_whitespace_sensitive(self):
        """Test that whitespace matters in password verification."""
        password = "password"
        hashed = get_password_hash(password)

        assert verify_password(plain_password=" password", hashed_password=hashed) is False
        assert verify_password(plain_password="password ", hashed_password=hashed) is False
        assert verify_password(plain_password="pass word", hashed_password=hashed) is False
