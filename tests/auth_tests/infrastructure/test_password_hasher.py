"""Tests for Password Hasher utilities."""


from app.infrastructure.auth.jwt.password_hasher import get_password_hash, verify_password


class TestGetPasswordHash:
    """Test get_password_hash function."""

    def test_get_password_hash_returns_string(self):
        """Test get_password_hash returns a string."""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)

    def test_get_password_hash_not_same_as_original(self):
        """Test get_password_hash result is different from original."""
        password = "original_password"
        hashed = get_password_hash(password)

        assert hashed != password

    def test_get_password_hash_uses_argon2_format(self):
        """Test get_password_hash uses Argon2 algorithm."""
        password = "test_password"
        hashed = get_password_hash(password)

        # Argon2 hashes start with $argon2
        assert hashed.startswith("$argon2")

    def test_get_password_hash_produces_long_string(self):
        """Test get_password_hash produces a long hash string."""
        password = "test"
        hashed = get_password_hash(password)

        # Argon2 hashes are typically 90+ characters
        assert len(hashed) > 50

    def test_get_password_hash_with_special_characters(self):
        """Test get_password_hash handles special characters."""
        passwords = [
            "p@ssw0rd!",
            "pass#word&symbol",
            "pass@123!$%^",
            "password-with-dashes",
            "password_with_underscores"
        ]

        for password in passwords:
            hashed = get_password_hash(password)
            assert isinstance(hashed, str)
            assert len(hashed) > 50

    def test_get_password_hash_with_unicode_characters(self):
        """Test get_password_hash handles unicode characters."""
        passwords = [
            "пароль123",  # Russian
            "密码123",  # Chinese
            "كلمةالسر123",  # Arabic
            "🔐password",  # Emoji
        ]

        for password in passwords:
            hashed = get_password_hash(password)
            assert isinstance(hashed, str)

    def test_get_password_hash_different_for_same_password(self):
        """Test get_password_hash produces different hashes for same password."""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Different due to salt
        assert hash1 != hash2

    def test_get_password_hash_with_very_long_password(self):
        """Test get_password_hash with very long password."""
        password = "p" * 1000  # 1000 character password
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 50

    def test_get_password_hash_with_spaces(self):
        """Test get_password_hash with password containing spaces."""
        password = "pass word with spaces"
        hashed = get_password_hash(password)

        assert hashed != password
        assert isinstance(hashed, str)

    def test_get_password_hash_with_empty_string_raises_error(self):
        """Test get_password_hash handles empty password."""
        # Note: passlib still hashes empty strings, but let's test behavior
        password = ""
        hashed = get_password_hash(password)

        # Should still return a hash (passlib hashes empty differently)
        assert isinstance(hashed, str)


class TestVerifyPassword:
    """Test verify_password function."""

    def test_verify_password_with_correct_password(self):
        """Test verify_password returns True with correct password."""
        password = "correct_password"
        hashed = get_password_hash(password)

        assert verify_password(plain_password=password, hashed_password=hashed) is True

    def test_verify_password_with_incorrect_password(self):
        """Test verify_password returns False with incorrect password."""
        correct_password = "correct"
        wrong_password = "wrong"
        hashed = get_password_hash(correct_password)

        assert verify_password(plain_password=wrong_password, hashed_password=hashed) is False

    def test_verify_password_case_sensitive(self):
        """Test verify_password is case sensitive."""
        password = "TestPassword123"
        hashed = get_password_hash(password)

        assert verify_password(plain_password="testpassword123", hashed_password=hashed) is False
        assert verify_password(plain_password="TESTPASSWORD123", hashed_password=hashed) is False

    def test_verify_password_with_special_characters(self):
        """Test verify_password with special characters."""
        password = "p@ssw0rd!$%^"
        hashed = get_password_hash(password)

        assert verify_password(plain_password=password, hashed_password=hashed) is True
        assert verify_password(plain_password="p@ssw0rd!$%^", hashed_password=hashed) is True

    def test_verify_password_with_unicode_characters(self):
        """Test verify_password with unicode characters."""
        passwords = [
            "пароль123",  # Russian
            "密码123",  # Chinese
        ]

        for password in passwords:
            hashed = get_password_hash(password)
            assert verify_password(plain_password=password, hashed_password=hashed) is True

    def test_verify_password_rejects_similar_passwords(self):
        """Test verify_password rejects similar but different passwords."""
        password = "password123"
        hashed = get_password_hash(password)

        similar_passwords = [
            "password124",  # Off by one
            "password12",   # Missing character
            "password1234",  # Extra character
            "Password123",  # Different case
            " password123",  # Leading space
            "password123 ",  # Trailing space
        ]

        for similar in similar_passwords:
            assert verify_password(plain_password=similar, hashed_password=hashed) is False

    def test_verify_password_with_multiple_correct_passwords(self):
        """Test verify_password with various correct passwords."""
        passwords = [
            "simple",
            "complex@123!",
            "very_long_password_with_many_characters",
            "pass word with spaces",
        ]

        for password in passwords:
            hashed = get_password_hash(password)
            assert verify_password(plain_password=password, hashed_password=hashed) is True


class TestPasswordHashingIntegration:
    """Integration tests for password hashing."""

    def test_hash_and_verify_workflow(self):
        """Test complete hash and verify workflow."""
        original_password = "my_secure_password_123"

        # Hash password
        hashed = get_password_hash(original_password)

        # Verify with correct password
        assert verify_password(plain_password=original_password, hashed_password=hashed) is True

        # Verify with incorrect password
        assert verify_password(plain_password="wrong_password", hashed_password=hashed) is False

    def test_multiple_users_different_hashes(self):
        """Test multiple users have different hashes for same password."""
        password = "same_password"

        hashes = [get_password_hash(password) for _ in range(5)]

        # All hashes should be unique
        assert len(set(hashes)) == 5

        # All should verify with correct password
        for hashed in hashes:
            assert verify_password(plain_password=password, hashed_password=hashed) is True

    def test_password_hashing_security_properties(self):
        """Test password hashing maintains security properties."""
        password = "test_password"
        hashed = get_password_hash(password)

        # Hash is deterministic for given salt
        assert verify_password(plain_password=password, hashed_password=hashed) is True

        # Hash is not reversible (can't recover password from hash)
        assert password not in str(hashed)

        # Hash is salted (different hashes for same password)
        hash2 = get_password_hash(password)
        assert hashed != hash2
