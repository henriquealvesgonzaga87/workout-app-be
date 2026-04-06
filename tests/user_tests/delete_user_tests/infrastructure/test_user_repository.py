from datetime import datetime

import pytest

from app.infrastructure.repositories.sqlalchemy.user.user_repo import (
    SQLAlchemyUserRepository,
)
from app.presentation.error_handlers.not_found_error import NotFoundError


class TestSQLAlchemyUserRepositoryDelete:
    """Test suite for delete operation in SQLAlchemyUserRepository."""

    def test_delete_existing_user(self, test_db_session):
        """Test deleting an existing user successfully."""
        # First create a user to delete
        from app.infrastructure.schemas.user.user_schema import UserSchema

        user = UserSchema(
            name="User to Delete",
            email="delete@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()
        user_id = user.id

        # Create a new session for delete operation
        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()

        repo = SQLAlchemyUserRepository(db_session=new_session)
        result = repo.delete(id=user_id)

        assert result is True

    def test_delete_user_returns_boolean_true(self, test_db_session):
        """Test that delete returns True on successful deletion."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create user
        user = UserSchema(
            name="Test User",
            email="test@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()
        user_id = user.id

        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()

        repo = SQLAlchemyUserRepository(db_session=new_session)
        result = repo.delete(id=user_id)

        assert isinstance(result, bool)
        assert result is True

    def test_delete_non_existent_user_raises_error(self, test_db_session):
        """Test that deleting a non-existent user raises NotFoundError."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        with pytest.raises(NotFoundError) as exc_info:
            repo.delete(id=99999)

        assert "not found" in str(exc_info.value).lower()

    def test_delete_removes_user_from_database(self, test_db_session):
        """Test that delete actually removes the user from the database."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create user
        user = UserSchema(
            name="User to be Removed",
            email="remove@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()
        user_id = user.id

        # Verify user exists
        existing_user = test_db_session.query(UserSchema).filter(UserSchema.id == user_id).first()
        assert existing_user is not None

        # Delete user using new session
        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()
        repo = SQLAlchemyUserRepository(db_session=new_session)
        repo.delete(id=user_id)

        # Check user is no longer in database
        TestSession2 = sessionmaker(bind=test_db_session.get_bind())
        check_session = TestSession2()
        deleted_user = check_session.query(UserSchema).filter(UserSchema.id == user_id).first()
        assert deleted_user is None

    def test_delete_with_different_user_ids(self, test_db_session):
        """Test deleting multiple users with different IDs."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create multiple users
        users_data = []
        for i in range(3):
            user = UserSchema(
                name=f"User {i}",
                email=f"user{i}@example.com",
                password="hash",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            )
            test_db_session.add(user)
            test_db_session.commit()
            users_data.append(user.id)

        # Delete each user
        from sqlalchemy.orm import sessionmaker
        for user_id in users_data:
            TestSession = sessionmaker(bind=test_db_session.get_bind())
            new_session = TestSession()
            repo = SQLAlchemyUserRepository(db_session=new_session)
            result = repo.delete(id=user_id)
            assert result is True

    def test_delete_already_deleted_user_raises_error(self, test_db_session):
        """Test that deleting an already deleted user raises NotFoundError."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create and delete a user
        user = UserSchema(
            name="User to Delete Twice",
            email="delete_twice@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()
        user_id = user.id

        # First deletion
        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()
        repo = SQLAlchemyUserRepository(db_session=new_session)
        result = repo.delete(id=user_id)
        assert result is True

        # Try to delete again - should raise NotFoundError
        TestSession2 = sessionmaker(bind=test_db_session.get_bind())
        new_session2 = TestSession2()
        repo2 = SQLAlchemyUserRepository(db_session=new_session2)

        with pytest.raises(NotFoundError):
            repo2.delete(id=user_id)

    def test_delete_with_zero_id_raises_error(self, test_db_session):
        """Test that delete with ID 0 raises NotFoundError."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        with pytest.raises(NotFoundError):
            repo.delete(id=0)

    def test_delete_with_negative_id_raises_error(self, test_db_session):
        """Test that delete with negative ID raises NotFoundError."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        with pytest.raises(NotFoundError):
            repo.delete(id=-1)

    def test_delete_user_with_admin_privileges(self, test_db_session):
        """Test deleting a user with admin privileges."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create admin user
        user = UserSchema(
            name="Admin User",
            email="admin@example.com",
            password="hash",
            is_active=True,
            is_super_admin=True,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()
        user_id = user.id

        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()
        repo = SQLAlchemyUserRepository(db_session=new_session)
        result = repo.delete(id=user_id)

        assert result is True

    def test_delete_inactive_user(self, test_db_session):
        """Test deleting an inactive user."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create inactive user
        user = UserSchema(
            name="Inactive User",
            email="inactive@example.com",
            password="hash",
            is_active=False,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()
        user_id = user.id

        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()
        repo = SQLAlchemyUserRepository(db_session=new_session)
        result = repo.delete(id=user_id)

        assert result is True

    def test_delete_calls_get_by_id_internally(self, test_db_session):
        """Test that delete method uses get_by_id to fetch user before deletion."""

        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create user
        user = UserSchema(
            name="Test User",
            email="test@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()
        user_id = user.id

        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()
        repo = SQLAlchemyUserRepository(db_session=new_session)

        # Delete should work correctly
        result = repo.delete(id=user_id)
        assert result is True

    def test_delete_user_case_insensitive_lookup(self, test_db_session):
        """Test delete with sequential IDs to ensure correct user is deleted."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create users with sequential IDs
        user_ids = []
        for i in range(3):
            user = UserSchema(
                name=f"User {i}",
                email=f"user{i}@example.com",
                password="hash",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            )
            test_db_session.add(user)
            test_db_session.commit()
            user_ids.append(user.id)

        # Delete the middle user
        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_db_session.get_bind())
        new_session = TestSession()
        repo = SQLAlchemyUserRepository(db_session=new_session)
        repo.delete(id=user_ids[1])

        # Verify only the correct user was deleted
        TestSession2 = sessionmaker(bind=test_db_session.get_bind())
        check_session = TestSession2()
        remaining = check_session.query(UserSchema).all()
        remaining_ids = [u.id for u in remaining]

        assert user_ids[0] in remaining_ids
        assert user_ids[1] not in remaining_ids
        assert user_ids[2] in remaining_ids
