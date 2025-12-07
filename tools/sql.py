import sqlite3
from langchain_core.tools import tool

@tool
def run_sqlite_query(query: str):
    """Run a sqlite query."""
    with sqlite3.connect("db.sqlite") as conn:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()

