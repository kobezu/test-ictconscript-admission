from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.responses import PlainTextResponse
from datetime import datetime

from models.entry import Entry
import database.database as db

app = FastAPI()

def get_db():
  con = db.get_db_connection()
  try:
    yield con
  finally:
    con.close()

@app.get("/")
def root():
  return {
    "name": "Unit Logbook API",
    "version": "1.0.0",
    "endpoints": {
      "entries": "/entries",
      "health": "/health",
      "docs": "/docs"
    },
  }

@app.get("/entries")
def list_entries(con=Depends(get_db)):
  return db.get_all(con)

@app.get("/entries/{id}")
def get_entry(id: str, con=Depends(get_db)):
  entry = db.get_entry(con, id)
  if entry is not None:
    print(entry)
    return entry
  else:
    raise HTTPException(status_code=404, detail=f"Entry {id} not found")

@app.post("/entries")
def create_entry(entry: Entry, con=Depends(get_db)):
  entry_data = dict(entry) # Convert Pydantic model to dictionary

  entry_data["id"] = db.count_entries(con) + 1 # Generate id
  entry_data["isoTime"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ') # Generate timestamp
  
  created_entry = db.insert_entry(con, entry_data) # Insert entry to database
  return created_entry

@app.get("/health", response_class=PlainTextResponse)
def get_health():
  return "OK"

# Respond with 204 - No content when page tries to load favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
def ignore_favicon():
  return Response(status_code=204)