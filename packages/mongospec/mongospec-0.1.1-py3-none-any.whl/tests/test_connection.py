import pytest
from mongospec._connection import _DatabaseConnection

@pytest.mark.asyncio
async def test_singleton_pattern():
    """Test that _DatabaseConnection follows singleton pattern."""
    conn1 = _DatabaseConnection()
    conn2 = _DatabaseConnection()
    assert conn1 is conn2

@pytest.mark.asyncio
async def test_connection_state(db_connection):
    """Test connection state management."""
    assert db_connection._is_connected is True
    assert db_connection._db is not None
    assert db_connection._client is not None
