import pytest
import motor.motor_asyncio
from mongospec._connection import _DatabaseConnection

@pytest.fixture(scope="session")
async def test_db():
    """Create a test database connection."""
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.test_mongospec
    
    # Clear all collections before tests
    await db.drop_database()
    
    yield db
    
    # Cleanup after tests
    await db.drop_database()
    client.close()

@pytest.fixture
async def db_connection(test_db):
    """Initialize the database connection for tests."""
    _DatabaseConnection._instance = None  # Reset singleton
    _DatabaseConnection._client = None
    _DatabaseConnection._db = None
    _DatabaseConnection._is_connected = False
    
    conn = _DatabaseConnection()
    await conn.connect(test_db)
    return conn
