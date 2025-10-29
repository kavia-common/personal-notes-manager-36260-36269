from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from ..models import Note
from ..schemas import NoteCreate, NoteUpdate

class NotesRepository:
    """In-memory repository for notes with thread safety."""

    def __init__(self) -> None:
        self._items: Dict[UUID, Note] = {}
        self._lock = RLock()

    # PUBLIC_INTERFACE
    def list_notes(self, offset: int = 0, limit: int = 100) -> Tuple[List[Note], int]:
        """Return a slice of notes and total count.
        
        Parameters:
            offset: number of items to skip.
            limit: maximum number of items to return.
        Returns:
            A tuple of (notes_list, total_count)
        """
        with self._lock:
            all_notes = list(self._items.values())
            total = len(all_notes)
            # Stable order: by created_at then id
            all_notes.sort(key=lambda n: (n.created_at, str(n.id)))
            sliced = all_notes[offset: offset + limit if limit is not None else None]
            return sliced, total

    # PUBLIC_INTERFACE
    def get_note(self, note_id: UUID) -> Optional[Note]:
        """Get a note by id or None if not found."""
        with self._lock:
            return self._items.get(note_id)

    # PUBLIC_INTERFACE
    def create_note(self, payload: NoteCreate) -> Note:
        """Create and return a new note."""
        now = datetime.now(timezone.utc)
        note = Note(
            id=uuid4(),
            title=payload.title,
            content=payload.content,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._items[note.id] = note
        return note

    # PUBLIC_INTERFACE
    def update_note(self, note_id: UUID, payload: NoteUpdate) -> Optional[Note]:
        """Update a note. Returns updated note or None if not found."""
        with self._lock:
            note = self._items.get(note_id)
            if note is None:
                return None
            updated = False
            if payload.title is not None:
                note.title = payload.title
                updated = True
            if payload.content is not None:
                note.content = payload.content
                updated = True
            if updated:
                note.updated_at = datetime.now(timezone.utc)
            return note

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: UUID) -> bool:
        """Delete a note by id. Returns True if existed and deleted."""
        with self._lock:
            return self._items.pop(note_id, None) is not None
