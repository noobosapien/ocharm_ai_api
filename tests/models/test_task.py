from sqlalchemy import Integer, Boolean, String, Text, DateTime, Enum  # noqa
from sqlalchemy.dialects.postgresql import TIMESTAMP  # noqa


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("task")


def test_model_structure_column_data_types(db_inspector):
    table = "task"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["time"]["type"], TIMESTAMP)
    assert isinstance(columns["severity"]["type"], Enum)
    assert isinstance(columns["description"]["type"], Text)
    assert isinstance(columns["user_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    table = "task"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "name": False,
        "time": False,
        "severity": False,
        "description": True,
        "user_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


def test_model_structure_column_constraints(db_inspector):
    table = "task"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "task_name_length_check" for constraint in constraints
    )


def test_model_structure_column_lengths(db_inspector):
    table = "task"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 200


def test_model_structure_foreign_key(db_inspector):
    table = "task"
    foreign_keys = db_inspector.get_foreign_keys(table)

    product_foreign_key = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["user_id"]),
        None,
    )

    assert product_foreign_key is not None
