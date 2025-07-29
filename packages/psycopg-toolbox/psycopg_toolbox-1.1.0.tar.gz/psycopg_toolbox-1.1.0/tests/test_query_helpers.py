"""Tests for query helper functions in psycopg-toolbox."""

import pytest
from psycopg.errors import Error

from psycopg_toolbox import (
    AlreadyExistsError,
    LoggingConnection,
    create_database,
    database_exists,
    drop_database,
    create_user,
    drop_user_or_role,
    autocommit,
)


@pytest.mark.asyncio
async def test_database_exists(
    psycopg_toolbox_empty_db: LoggingConnection,
) -> None:
    """Test database_exists function."""
    # Test with non-existent database
    assert not await database_exists(
        psycopg_toolbox_empty_db, "psycopg_toolbox_test_nonexistent"
    )

    # Test with existing database (the test database)
    dbname = psycopg_toolbox_empty_db.info.dbname
    assert await database_exists(psycopg_toolbox_empty_db, dbname)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "encoding,template,ignore_exists,should_exist,expected_result,owner,test_id",
    [
        (None, None, False, False, True, None, "basic_create"),
        ("UTF8", None, False, False, True, None, "with_encoding"),
        (None, "template0", False, False, True, None, "with_template"),
        ("UTF8", "template0", False, False, True, None, "with_both"),
        (None, None, True, True, False, None, "ignore_existing"),
        (None, None, False, False, True, "psycopg_toolbox_test_owner", "with_owner"),
    ],
    ids=[
        "basic_create",
        "with_encoding",
        "with_template",
        "with_both",
        "ignore_existing",
        "with_owner",
    ],
)
async def test_create_database(
    psycopg_toolbox_empty_db: LoggingConnection,
    encoding: str | None,
    template: str | None,
    ignore_exists: bool,
    should_exist: bool,
    expected_result: bool,
    owner: str | None,
    test_id: str,
) -> None:
    """Test create_database function.

    Args:
        psycopg_toolbox_empty_db: Test database connection
        encoding: Character encoding to use
        template: Template database to use
        ignore_exists: Whether to ignore if database exists
        should_exist: Whether to create database before testing
        expected_result: Expected return value
        owner: Role name to set as database owner
        test_id: Unique identifier for the test case
    """
    test_db = f"psycopg_toolbox_test_create_{test_id}"

    async with autocommit(psycopg_toolbox_empty_db):
        try:
            # Create database first if should_exist is True
            if should_exist:
                await create_database(psycopg_toolbox_empty_db, test_db)

            if owner:
                await create_user(
                    conn=psycopg_toolbox_empty_db, name=owner, error_if_exists=False
                )

            # Test creation
            result = await create_database(
                psycopg_toolbox_empty_db,
                test_db,
                encoding=encoding,
                template=template,
                ignore_exists=ignore_exists,
                owner=owner,
            )
            assert result == expected_result

            # If owner was specified, verify it was set correctly
            if owner:
                owner_result = await psycopg_toolbox_empty_db.execute(
                    "SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname = %s",
                    [test_db],
                )
                db_owner = await owner_result.fetchone()
                assert db_owner is not None
                assert db_owner[0] == owner

        finally:
            # Clean up
            await drop_database(psycopg_toolbox_empty_db, test_db, ignore_missing=True)
            if owner:
                await drop_user_or_role(psycopg_toolbox_empty_db, owner)


@pytest.mark.asyncio
async def test_create_database_already_exists(
    psycopg_toolbox_empty_db: LoggingConnection,
) -> None:
    """Test create_database raises AlreadyExistsError when database exists."""
    test_db = "psycopg_toolbox_test_create_exists"
    try:
        # Create database first
        await create_database(psycopg_toolbox_empty_db, test_db)

        # Try to create it again
        with pytest.raises(AlreadyExistsError):
            await create_database(psycopg_toolbox_empty_db, test_db)
    finally:
        # Clean up
        await drop_database(psycopg_toolbox_empty_db, test_db, ignore_missing=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ignore_missing,should_exist",
    [
        (False, True),  # Drop existing
        (True, False),  # Ignore missing
    ],
    ids=[
        "drop_existing",
        "ignore_missing",
    ],
)
async def test_drop_database(
    psycopg_toolbox_empty_db: LoggingConnection,
    ignore_missing: bool,
    should_exist: bool,
) -> None:
    """Test drop_database function.

    Args:
        psycopg_toolbox_empty_db: Test database connection
        ignore_missing: Whether to ignore if database doesn't exist
        should_exist: Whether to create database before testing
    """
    test_db = "psycopg_toolbox_test_drop"
    try:
        # Create database first if should_exist is True
        if should_exist:
            await create_database(psycopg_toolbox_empty_db, test_db)

        # Test dropping
        await drop_database(
            psycopg_toolbox_empty_db,
            test_db,
            ignore_missing=ignore_missing,
        )
    finally:
        # Extra cleanup in case test fails before drop
        await drop_database(psycopg_toolbox_empty_db, test_db, ignore_missing=True)


@pytest.mark.asyncio
async def test_drop_database_with_connections(
    psycopg_toolbox_empty_db: LoggingConnection,
) -> None:
    """Test drop_database terminates connections before dropping."""
    test_db = "psycopg_toolbox_test_drop_with_conns"
    try:
        # Create test database
        await create_database(psycopg_toolbox_empty_db, test_db)

        # Create a connection to the test database
        async with await LoggingConnection.connect(
            dbname=test_db,
            user=psycopg_toolbox_empty_db.info.user,
            password=psycopg_toolbox_empty_db.info.password,
            host=psycopg_toolbox_empty_db.info.host,
            port=psycopg_toolbox_empty_db.info.port,
        ) as conn:
            # Try to drop the database while it has a connection
            await drop_database(psycopg_toolbox_empty_db, test_db)

            # Verify the connection was terminated
            with pytest.raises(Error):
                await conn.execute("SELECT 1")
    finally:
        await drop_database(psycopg_toolbox_empty_db, test_db, ignore_missing=True)
