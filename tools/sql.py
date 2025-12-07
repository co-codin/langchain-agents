import sqlite3
from langchain_core.tools import tool

conn = sqlite3.connect("db.sqlite")

@tool
def run_sqlite_query(query):
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()

