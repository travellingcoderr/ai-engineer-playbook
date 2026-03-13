
from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MCP Gateway Running"}

@app.get("/query")
def query_db(sql: str):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return {"results": rows}
