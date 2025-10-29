# personal-notes-manager-36260-36269

Notes Backend (FastAPI)
- App entrypoint: src.api.main:app
- Port: 3001
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

Run locally
1. cd notes_backend
2. Install dependencies:
   pip install -r requirements.txt
3. Start server on port 3001:
   uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

Endpoints
- GET /           Health check
- GET /notes      List notes (query: limit, offset)
- POST /notes     Create note (title, content)
- GET /notes/{id} Get note by UUID
- PUT /notes/{id} Update note (title?, content?)
- DELETE /notes/{id} Delete note (204 on success)

Schemas
- NoteCreate: title, content
- NoteUpdate: title?, content?
- NoteOut: id, title, content, created_at, updated_at

Repository
- In-memory NotesRepository with DI dependency get_repository() in src/db/__init__.py
