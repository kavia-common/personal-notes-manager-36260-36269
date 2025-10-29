from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    title: str = Field(..., description="Title of the note", min_length=1)
    content: str = Field(..., description="Content/body of the note")

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating an existing note. All fields optional."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1)
    content: Optional[str] = Field(None, description="Updated content/body of the note")

# PUBLIC_INTERFACE
class NoteOut(BaseModel):
    """Schema returned by the API representing a note."""
    id: UUID = Field(..., description="Unique identifier of the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content/body of the note")
    created_at: datetime = Field(..., description="Creation timestamp in UTC")
    updated_at: datetime = Field(..., description="Last update timestamp in UTC")
