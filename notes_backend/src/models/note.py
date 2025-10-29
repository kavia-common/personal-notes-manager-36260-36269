from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Note:
    """Domain model for notes used by repository layer."""
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
