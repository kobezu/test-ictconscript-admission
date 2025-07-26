import sqlite3

def get_db_connection():
  con = sqlite3.connect("entries.db")
  return con
    
def count_entries(con):
  cur = con.cursor()
  cur.execute("SELECT * FROM entries")
  return len(cur.fetchall())

def get_entry(con, id):
  cur = con.cursor()
  cur.execute("SELECT * FROM entries WHERE id = :id", {'id': id})
  return cur.fetchone()
  
def get_all(con):
  cur = con.cursor()
  cur.execute("SELECT * FROM entries ORDER BY isoTime DESC")
  return cur.fetchall()
  
def insert_entry(con, entry):
  cur = con.cursor()
  with con:
    cur.execute("""
                INSERT INTO entries VALUES (
                :id, :title, :body, :isoTime, :lat, :lon
                )""", 
                {
                  'id': entry["id"], 
                  'title': entry["title"], 
                  'body': entry["body"],
                  'isoTime': entry["isoTime"],
                  'lat': entry["lat"],
                  'lon': entry["lon"]
                })
  return get_entry(con, cur.lastrowid)