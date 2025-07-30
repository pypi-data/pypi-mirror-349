
import asyncio
import os
import pytest
import mongojet
from mongospec import init, is_connected
from mongospec.document import MongoDocument

TEST_DB_NAME = "mongospec_test"

# Ensure pytest-asyncio uses the same session loop across fixtures
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def mongo_database(event_loop):
    """Provide a real MongoDB database connection for tests.

    The URI can be configured via the MONGODB_URI environment variable.
    By default it connects to mongodb://localhost:27017 and creates a fresh
    temporary database named ``mongospec_test`` which is dropped when tests finish.

    Make sure a MongoDB server is running locally or adjust the URI accordingly.
    """
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = mongojet.Client(uri)  # type: ignore[attr-defined]
    db = client[TEST_DB_NAME]
    # Drop the database in case it exists from previous runs
    yield db
    # Cleanup
    await db.drop()
    await client.close()

@pytest.fixture(scope="session")
async def init_connection(mongo_database):
    """Initialize mongospec connection once per test session."""
    await init(mongo_database)
    assert is_connected()
    yield
    # no explicit disconnect function exposed; database cleanup done in mongo_database fixture

class User(MongoDocument):
    """Simple document model used in tests."""
    __collection_name__ = "users"

    name: str
    age: int

@pytest.fixture()
def user_cls(init_connection):
    """Return the User model class."""
    return User
