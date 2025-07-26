from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.responses import RedirectResponse, PlainTextResponse
from pydantic import BaseModel, Field
from datetime import datetime
import database as db

class Entry(BaseModel):
  title: str = Field(max_length=120)
  body: str
  lat: float | None = None
  lon: float | None = None

def get_db():
  con = db.get_db_connection()
  try:
    yield con
  finally:
    con.close()

app = FastAPI()

@app.get("/")
def root():
  return RedirectResponse(url="/docs") 

@app.get("/entries")
def list_entries(con=Depends(get_db)):
  return db.get_all(con)

@app.get("/entries/{id}")
def get_entry(id: str, con=Depends(get_db)):
  entry = db.get_entry(con, id)
  if entry is not None:
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

@app.get("/favicon.ico", include_in_schema=False)
def ignore_favicon():
  return Response(status_code=204)