"""Tests for role management functions (integration, real DB)."""

import pytest
import secrets

from psycopg_toolbox import (
    create_user,
    create_role,
    drop_user_or_role,
    get_current_user,
    user_or_role_exists,
)
from psycopg_toolbox import AlreadyExistsError


@pytest.mark.asyncio
async def test_user_or_role_exists(psycopg_toolbox_empty_db):
    """Test user_or_role_exists with real DB."""
    conn = psycopg_toolbox_empty_db
    name = f"toolbox_test_user_{secrets.token_hex(4)}"
    # Should not exist
    assert not await user_or_role_exists(conn, name)
    # Create user
    await create_user(conn=conn, name=name)
    assert await user_or_role_exists(conn, name)
    # Cleanup
    await drop_user_or_role(conn, name, ignore_missing=True)


@pytest.mark.asyncio
async def test_create_user(psycopg_toolbox_empty_db):
    """Test create_user with real DB."""
    conn = psycopg_toolbox_empty_db
    name = f"toolbox_test_user_{secrets.token_hex(4)}"
    parent = f"toolbox_test_parent_{secrets.token_hex(4)}"
    # Create parent role
    await create_role(conn=conn, name=parent)
    # Create user with password and parent role
    await create_user(conn=conn, name=name, password="pw", parent_role=parent)
    assert await user_or_role_exists(conn, name)
    # Try to create again, should raise
    with pytest.raises(AlreadyExistsError):
        await create_user(conn=conn, name=name)
    # Should not raise if error_if_exists is False
    await create_user(conn=conn, name=name, error_if_exists=False)
    # Create user with no password
    name2 = f"toolbox_test_user_{secrets.token_hex(4)}"
    await create_user(conn=conn, name=name2)
    assert await user_or_role_exists(conn, name2)
    # Create user with same name as parent role (should not error)
    name3 = f"toolbox_test_user_{secrets.token_hex(4)}"
    await create_user(conn=conn, name=name3, parent_role=name3)
    assert await user_or_role_exists(conn, name3)
    # Cleanup
    await drop_user_or_role(conn, name, ignore_missing=True)
    await drop_user_or_role(conn, name2, ignore_missing=True)
    await drop_user_or_role(conn, name3, ignore_missing=True)
    await drop_user_or_role(conn, parent, ignore_missing=True)


@pytest.mark.asyncio
async def test_create_role(psycopg_toolbox_empty_db):
    """Test create_role with real DB."""
    conn = psycopg_toolbox_empty_db
    name = f"toolbox_test_role_{secrets.token_hex(4)}"
    parent = f"toolbox_test_parent_{secrets.token_hex(4)}"
    # Create parent role
    await create_role(conn=conn, name=parent)
    # Create role with parent
    await create_role(conn=conn, name=name, parent_role=parent)
    assert await user_or_role_exists(conn, name)
    # Try to create again, should raise
    with pytest.raises(AlreadyExistsError):
        await create_role(conn=conn, name=name)
    # Should not raise if error_if_exists is False
    await create_role(conn=conn, name=name, error_if_exists=False)
    # Create role with same name as parent role (should not error)
    name2 = f"toolbox_test_role_{secrets.token_hex(4)}"
    await create_role(conn=conn, name=name2, parent_role=name2)
    assert await user_or_role_exists(conn, name2)
    # Cleanup
    await drop_user_or_role(conn, name, ignore_missing=True)
    await drop_user_or_role(conn, name2, ignore_missing=True)
    await drop_user_or_role(conn, parent, ignore_missing=True)


@pytest.mark.asyncio
async def test_drop_user_or_role(psycopg_toolbox_empty_db):
    """Test drop_user_or_role with real DB."""
    conn = psycopg_toolbox_empty_db
    name = f"toolbox_test_role_{secrets.token_hex(4)}"
    # Drop non-existent role (should not error with ignore_missing)
    await drop_user_or_role(conn, name, ignore_missing=True)
    # Create and drop
    await create_role(conn=conn, name=name)
    assert await user_or_role_exists(conn, name)
    await drop_user_or_role(conn, name)
    assert not await user_or_role_exists(conn, name)


@pytest.mark.asyncio
async def test_get_current_user(psycopg_toolbox_empty_db):
    """Test get_current_user with real DB."""
    conn = psycopg_toolbox_empty_db
    user = await get_current_user(conn)
    # Should match the connection user
    assert user == conn.info.user
