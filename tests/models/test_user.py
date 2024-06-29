from sqlalchemy import Integer, Boolean, String, Text, DateTime, Enum, ARRAY  # noqa


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("user")


def test_model_structure_column_data_types(db_inspector):
    table = "user"

    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    # assert isinstance(columns["associated"]["type"], ARRAY)
    assert isinstance(columns["role"]["type"], Enum)


def test_model_structure_nullable_constraints(db_inspector):
    table = "user"
    columns = db_inspector.get_columns(table)

    expected_nullable = {"id": False, "name": False, "role": False}

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


def test_model_structure_column_constraints(db_inspector):
    table = "user"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "user_name_length_check" for constraint in constraints
    )


def test_model_structure_default_values(db_inspector):
    table = "user"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["role"]["default"] == "'primary'::role_enum"


def test_model_structure_column_lengths(db_inspector):
    table = "user"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100
