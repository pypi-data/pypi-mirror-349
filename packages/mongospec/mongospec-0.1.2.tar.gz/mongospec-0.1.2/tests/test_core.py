
import pytest
import mongospec

@pytest.mark.asyncio
async def test_get_collection(user_cls):
    collection = mongospec.get_collection("users")
    # Collection type is not strictly asserted here to avoid coupling to motor types
    assert hasattr(collection, "insert_one")
