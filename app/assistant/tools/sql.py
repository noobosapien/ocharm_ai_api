from typing import List

from langchain.tools import Tool
from pydantic.v1 import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db_connection import SessionLocal

db = SessionLocal()


def list_tables(db: Session):
    command = text(
        "tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');"
    )
    tables = db.query(command).all()

    table_list = []

    for table in tables:
        if table[0] != "alembic_version":
            table_list.append(table[0])

    return table_list


def run_postgres_query(query):
    try:
        # query = query.lower()
        # query.replace("select", "")
        # query = query[6:]
        query += ";"
        print("\n\n\n\n\n\n\n\n\n", query, "\n\n\n\n\n\n\n\n\n")
        command = text(query)
        result = db.execute(command).all()

        return result
    except Exception as e:
        print("\n\n\n\n\n\n\n\n\n", e, "\n\n\n\n\n\n\n\n\n")
        return f"The following error occurred: {str(e)}"


class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_postgres_query",
    description="Run a postgres query",
    func=run_postgres_query,
    args_schema=RunQueryArgsSchema,
)


def describe_tables(table_names):
    try:
        tables = ", ".join("'" + item + "'" for item in table_names)

        rows = text(
            f'(table_name, column_name) FROM INFORMATION_SCHEMA.COLUMNS WHERE CAST("table_schema" AS text) = \'public\' AND CAST("table_name" AS text) IN ({tables});'
        )

        result = db.query(rows).all()
        return result
    except Exception as e:
        return f"The following error occurred: {str(e)}"


class DescribeTableArgsSchema(BaseModel):
    table_names: List[str]


describes_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns a schema of those tables",
    func=describe_tables,
    args_schema=DescribeTableArgsSchema,
)
