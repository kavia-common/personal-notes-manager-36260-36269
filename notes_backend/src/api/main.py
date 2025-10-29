from typing import List
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from ..db import get_repository, NotesRepository
from ..schemas import NoteCreate, NoteUpdate, NoteOut

openapi_tags = [
    {"name": "health", "description": "Service health and diagnostics"},
    {"name": "notes", "description": "CRUD operations for notes"},
]

app = FastAPI(
    title="Notes Backend API",
    description="FastAPI service that provides CRUD endpoints for managing personal notes.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

# Keep existing CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/", tags=["health"], summary="Health Check")
def health_check():
    """Health check endpoint to verify the service is running.
    
    Returns:
        JSON object with a simple message.
    """
    return {"message": "Healthy"}

# Helpers to convert domain model to schema
def to_note_out(note) -> NoteOut:
    return NoteOut(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )

# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[NoteOut],
    summary="List notes",
    description="Retrieve a paginated list of notes.",
    tags=["notes"],
)
def list_notes(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of notes to return"),
    offset: int = Query(0, ge=0, description="Number of notes to skip"),
    repo: NotesRepository = Depends(get_repository),
):
    """List notes with pagination.
    
    Parameters:
        limit: Maximum number of notes to return (1-1000).
        offset: Number of notes to skip.
    Returns:
        A list of notes (NoteOut).
    """
    notes, _total = repo.list_notes(offset=offset, limit=limit)
    return [to_note_out(n) for n in notes]

# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note and return it.",
    tags=["notes"],
)
def create_note(
    payload: NoteCreate,
    repo: NotesRepository = Depends(get_repository),
):
    """Create a new note."""
    note = repo.create_note(payload)
    return to_note_out(note)

# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=NoteOut,
    summary="Get a note",
    description="Retrieve a note by its UUID.",
    tags=["notes"],
)
def get_note(
    note_id: UUID,
    repo: NotesRepository = Depends(get_repository),
):
    """Get a note by ID or return 404."""
    note = repo.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return to_note_out(note)

# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=NoteOut,
    summary="Update a note",
    description="Update an existing note by its UUID and return the updated note.",
    tags=["notes"],
)
def update_note(
    note_id: UUID,
    payload: NoteUpdate,
    repo: NotesRepository = Depends(get_repository),
):
    """Update a note by ID or return 404."""
    note = repo.update_note(note_id, payload)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return to_note_out(note)

# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its UUID. Returns 204 on success or 404 if not found.",
    tags=["notes"],
)
def delete_note(
    note_id: UUID,
    repo: NotesRepository = Depends(get_repository),
):
    """Delete a note by ID. Returns 204 No Content on success."""
    deleted = repo.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    # Returning None ensures 204 No Content
    return None
