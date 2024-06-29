from typing import List

from langchain.tools import Tool
from pydantic.v1 import BaseModel


def list_tables():
    pass


def run_postgres_query(query):
    pass


class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_postgres_query",
    description="Run a postgres query",
    func=run_postgres_query,
    args_schema=RunQueryArgsSchema,
)


def describe_tables(table_names):
    pass


class DescribeTableArgsSchema(BaseModel):
    table_names: List[str]


describes_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns a schema of those tables",
    func=describe_tables,
    args_schema=DescribeTableArgsSchema,
)
