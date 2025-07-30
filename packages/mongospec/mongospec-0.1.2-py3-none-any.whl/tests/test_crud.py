
import asyncio
from bson import ObjectId
import pytest

@pytest.mark.asyncio
async def test_insert_and_find(user_cls):
    # Insert a document
    user = await user_cls(name="Alice", age=25).insert()
    assert isinstance(user._id, ObjectId)

    # Find the same document
    found = await user_cls.find_one({"_id": user._id})
    assert found is not None
    assert found.name == "Alice"
    assert found.age == 25

@pytest.mark.asyncio
async def test_count_documents(user_cls):
    # Ensure there is at least one document
    await user_cls(name="Bob", age=30).insert()
    count = await user_cls.count_documents()
    assert count >= 1

@pytest.mark.asyncio
async def test_update_document(user_cls):
    # Insert then update
    user = await user_cls(name="Charlie", age=20).insert()
    modified = await user_cls.update_one({"_id": user._id}, {"$set": {"age": 21}})
    assert modified == 1
    updated = await user_cls.find_one({"_id": user._id})
    assert updated.age == 21

@pytest.mark.asyncio
async def test_delete_document(user_cls):
    user = await user_cls(name="Dave", age=40).insert()
    deleted = await user_cls.delete_one({"_id": user._id})
    assert deleted == 1
    remaining = await user_cls.find_one({"_id": user._id})
    assert remaining is None

@pytest.mark.asyncio
async def test_validate_document_type_error(user_cls):
    with pytest.raises(TypeError):
        await user_cls.insert_one("not a document")  # type: ignore[arg-type]
