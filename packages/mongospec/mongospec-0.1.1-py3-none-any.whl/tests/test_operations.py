import pytest
from datetime import datetime
from mongospec.document.document import MongoDocument
from mongospec._connection import _DatabaseConnection

class TestDocument(MongoDocument):
    """Test document class."""
    __collection_name__ = "test_documents"
    
    id: ObjectId
    name: str
    created_at: datetime

@pytest.mark.asyncio
async def test_insert_operation(db_connection):
    """Test document insertion."""
    doc = TestDocument(id=ObjectId(), name="test", created_at=datetime.utcnow())
    result = await doc.insert()
    assert result.inserted_id == doc.id

@pytest.mark.asyncio
async def test_find_operation(db_connection):
    """Test document finding."""
    doc = TestDocument(id=ObjectId(), name="test", created_at=datetime.utcnow())
    await doc.insert()
    
    found = await TestDocument.find_one({"name": "test"})
    assert found is not None
    assert found.name == "test"

@pytest.mark.asyncio
async def test_update_operation(db_connection):
    """Test document update."""
    doc = TestDocument(id=ObjectId(), name="test", created_at=datetime.utcnow())
    await doc.insert()
    
    updated = await TestDocument.update_one({"name": "test"}, {"$set": {"name": "updated"}})
    assert updated.modified_count == 1
    
    found = await TestDocument.find_one({"name": "updated"})
    assert found is not None

@pytest.mark.asyncio
async def test_delete_operation(db_connection):
    """Test document deletion."""
    doc = TestDocument(id=ObjectId(), name="test", created_at=datetime.utcnow())
    await doc.insert()
    
    deleted = await TestDocument.delete_one({"name": "test"})
    assert deleted.deleted_count == 1
    
    found = await TestDocument.find_one({"name": "test"})
    assert found is None
