import pytest
from datetime import datetime
from mongospec.document.document import MongoDocument
from bson import ObjectId

class TestDocument(MongoDocument):
    """Test document class."""
    __collection_name__ = "test_documents"
    
    id: ObjectId
    name: str
    created_at: datetime

@pytest.mark.asyncio
async def test_document_creation():
    """Test document creation with valid data."""
    doc = TestDocument(id=ObjectId(), name="test", created_at=datetime.utcnow())
    assert doc.name == "test"
    assert isinstance(doc.id, ObjectId)
    assert isinstance(doc.created_at, datetime)

@pytest.mark.asyncio
async def test_document_invalid_id():
    """Test document creation with invalid ObjectId."""
    with pytest.raises(ValueError):
        TestDocument(id="invalid_id", name="test", created_at=datetime.utcnow())

@pytest.mark.asyncio
async def test_document_default_dec_hook():
    """Test default decoding hook."""
    oid = ObjectId()
    doc = TestDocument(id=oid, name="test", created_at=datetime.utcnow())
    
    # Test string to ObjectId conversion
    decoded = TestDocument.decode({"id": str(oid), "name": "test", "created_at": datetime.utcnow()})
    assert decoded.id == oid

@pytest.mark.asyncio
async def test_document_enc_hook_error():
    """Test that encoding hook raises NotImplementedError."""
    doc = TestDocument(id=ObjectId(), name="test", created_at=datetime.utcnow())
    with pytest.raises(NotImplementedError):
        doc.encode()
