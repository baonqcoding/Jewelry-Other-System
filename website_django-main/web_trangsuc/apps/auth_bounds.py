"""
Ranh gioi (boundary) cho Register / Login — dung de thiet ke BVA.

| Field       | Min | Max | Bat buoc | Ghi chu                          |
|-------------|-----|-----|----------|----------------------------------|
| username    | 1   | 20  | Yes      | chi chu/so/_ , khong khoang trang|
| password    | 8   | 32  | Yes      |                                  |
| email       | 5   | 50  | Yes (DK) | dang co @                        |
| first_name  | 0   | 30  | No       | cho phep rong                    |
| last_name   | 0   | 30  | No       | cho phep rong                    |
"""
from __future__ import annotations

import re
from typing import Any

USERNAME_MIN_LENGTH = 1
USERNAME_MAX_LENGTH = 20
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 32
EMAIL_MIN_LENGTH = 5
EMAIL_MAX_LENGTH = 50
FIRST_NAME_MIN_LENGTH = 0
FIRST_NAME_MAX_LENGTH = 30
LAST_NAME_MIN_LENGTH = 0
LAST_NAME_MAX_LENGTH = 30

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _as_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def validate_username(username: Any) -> str | None:
    """Tra ve message loi hoac None neu hop le."""
    if username is None or (isinstance(username, str) and username == ""):
        return f"Username is required (length {USERNAME_MIN_LENGTH}-{USERNAME_MAX_LENGTH})"
    text = _as_str(username)
    if text is None:
        return f"Username is required (length {USERNAME_MIN_LENGTH}-{USERNAME_MAX_LENGTH})"
    n = len(text)
    if n < USERNAME_MIN_LENGTH or n > USERNAME_MAX_LENGTH:
        return f"Username must be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH} characters"
    if not USERNAME_PATTERN.fullmatch(text):
        return "Username may only contain letters, numbers, and underscore"
    return None


def validate_password(password: Any) -> str | None:
    if password is None or (isinstance(password, str) and password == ""):
        return f"Password is required (length {PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH})"
    text = _as_str(password)
    if text is None:
        return f"Password is required (length {PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH})"
    n = len(text)
    if n < PASSWORD_MIN_LENGTH or n > PASSWORD_MAX_LENGTH:
        return f"Password must be between {PASSWORD_MIN_LENGTH} and {PASSWORD_MAX_LENGTH} characters"
    return None


def validate_email(email: Any) -> str | None:
    if email is None or (isinstance(email, str) and email == ""):
        return f"Email is required (length {EMAIL_MIN_LENGTH}-{EMAIL_MAX_LENGTH})"
    text = _as_str(email)
    if text is None:
        return f"Email is required (length {EMAIL_MIN_LENGTH}-{EMAIL_MAX_LENGTH})"
    n = len(text)
    if n < EMAIL_MIN_LENGTH or n > EMAIL_MAX_LENGTH:
        return f"Email must be between {EMAIL_MIN_LENGTH} and {EMAIL_MAX_LENGTH} characters"
    if not EMAIL_PATTERN.fullmatch(text):
        return "Email format is invalid"
    return None


def validate_optional_name(value: Any, field: str, min_len: int, max_len: int) -> str | None:
    if value is None:
        return None
    text = _as_str(value)
    if text is None:
        return None
    n = len(text)
    if n < min_len or n > max_len:
        return f"{field} must be between {min_len} and {max_len} characters"
    return None


def validate_register_payload(data: dict) -> list[str]:
    """Tra ve list loi; rong = hop le."""
    errors: list[str] = []
    for msg in (
        validate_username(data.get("username")),
        validate_password(data.get("password")),
        validate_email(data.get("email")),
        validate_optional_name(
            data.get("first_name"),
            "first_name",
            FIRST_NAME_MIN_LENGTH,
            FIRST_NAME_MAX_LENGTH,
        ),
        validate_optional_name(
            data.get("last_name"),
            "last_name",
            LAST_NAME_MIN_LENGTH,
            LAST_NAME_MAX_LENGTH,
        ),
    ):
        if msg:
            errors.append(msg)
    return errors


def validate_login_payload(data: dict) -> list[str]:
    errors: list[str] = []
    for msg in (
        validate_username(data.get("username")),
        validate_password(data.get("password")),
    ):
        if msg:
            errors.append(msg)
    return errors
