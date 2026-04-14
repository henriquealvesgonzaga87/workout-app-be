from typing import Any

from app.presentation.error_handlers.forbidden_error import ForbiddenError


def verify_token_payload_user_role(access_token_payload: dict[str, Any]) -> bool:
    payload_role = access_token_payload.get("role")

    if payload_role is False:
        raise ForbiddenError("You don't have permissions for this operation")

    return True


def verify_token_payload_user_id(id: int, access_token_payload: dict[str, Any]) -> None:
    user_payload_id = access_token_payload.get("id")
    is_admin = access_token_payload.get("role", False)

    # Allow if user is admin (can access any user) or if the ID matches their own ID
    if not is_admin and user_payload_id != id:
        raise ForbiddenError("Permission denied")
