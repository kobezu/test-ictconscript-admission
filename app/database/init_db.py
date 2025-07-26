import sqlite3
from database import insert_entry
import json

def init_db():
  con = sqlite3.connect("entries.db")

  # Create a db for entries
  con.cursor().execute("""
            CREATE TABLE IF NOT EXISTS entries (
            id text,
            title text,
            body text,
            isoTime text,
            lat real,
            lon real
            )""")

  # Add log entries from data.json to the db
  with open("../../sample-data/data.json") as f:
    data = json.load(f)
    for entry in data:
      insert_entry(con, entry)

  con.close()

if __name__ == "__main__":
  init_db()