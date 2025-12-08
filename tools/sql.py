import sqlite3
from langchain_core.tools import tool
from pydantic import BaseModel
from typing import List

def list_tables():
    with sqlite3.connect("db.sqlite") as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rows = c.fetchall()
        return "\n".join(row[0] for row in rows if row[0] is not None)

class RunQueryArgsSchema(BaseModel):
    query: str


class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

@tool(
    args_schema=RunQueryArgsSchema
)
def run_sqlite_query(query: str):
    """Run a sqlite query."""
    with sqlite3.connect("db.sqlite") as conn:
        c = conn.cursor()

        try:
            c.execute(query)
            return c.fetchall()
        except sqlite3.OperationalError as err:
            return f"The following error occurred: {str(err)}"

@tool(
    args_schema=DescribeTablesArgsSchema
)
def describe_tables(table_names):
    """Given a list of table names, returns the schema of those tables"""
    with sqlite3.connect("db.sqlite") as conn:
        c = conn.cursor()
        tables = ', '.join("'" + table + "'" for table in table_names)
        rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
        return '\n'.join(row[0] for row in rows if row[0] is not None)