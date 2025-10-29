from .notes_repository import NotesRepository

# A simple module-level singleton repository instance for the app lifetime.
_repo_instance: NotesRepository | None = None

# PUBLIC_INTERFACE
def get_repository() -> NotesRepository:
    """Dependency provider returning the singleton NotesRepository instance."""
    global _repo_instance
    if _repo_instance is None:
        _repo_instance = NotesRepository()
    return _repo_instance

__all__ = ["NotesRepository", "get_repository"]
