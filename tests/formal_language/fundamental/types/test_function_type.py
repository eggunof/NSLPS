import pytest

from nslps.formal_language.fundamentals.types import BaseType, FunctionType, TypeExpression


@pytest.mark.parametrize(
    "arg_types, result_type",
    [
        ((BaseType("a"), BaseType("b")), BaseType("t")),
        ((BaseType("t"),), BaseType("t")),
        ((BaseType("t"), BaseType("t")), BaseType("t")),
    ],
)
def test_create_function_type_with_valid_data_returns_function_type(
    arg_types: tuple[TypeExpression, ...], result_type: TypeExpression
) -> None:
    """Test creation of function type with valid data."""
    function_type = FunctionType(arg_types, result_type)
    assert function_type.arg_types == arg_types
    assert function_type.result_type == result_type


def test_create_function_type_with_empty_arg_types_raises_value_error() -> None:
    """Test creation of function type with empty argument types."""
    with pytest.raises(ValueError):
        FunctionType(tuple(), BaseType("t"))


@pytest.mark.parametrize(
    "arg_types, result_type, expected_str",
    [
        ((BaseType("a"), BaseType("b")), BaseType("t"), "<[a, b], t>"),
        ((BaseType("t"),), BaseType("t"), "<[t], t>"),
        ((BaseType("t"), BaseType("t")), BaseType("t"), "<[t, t], t>"),
    ],
)
def test_str_function_type_with_valid_data_returns_valid_str(
    arg_types: tuple[TypeExpression, ...], result_type: TypeExpression, expected_str: str
) -> None:
    """Test string representation of function types."""
    function_type = FunctionType(arg_types, result_type)
    assert str(function_type) == expected_str


@pytest.mark.parametrize(
    "arg_types, result_type",
    [
        ((BaseType("a"), BaseType("b")), BaseType("t")),
        ((BaseType("t"),), BaseType("t")),
        ((BaseType("t"), BaseType("t")), BaseType("t")),
    ],
)
def test_function_type_equality_with_valid_data_returns_true(
    arg_types: tuple[TypeExpression, ...], result_type: TypeExpression
) -> None:
    """Test equality of function types."""
    function_type = FunctionType(arg_types, result_type)
    other_function_type = FunctionType(arg_types, result_type)
    assert function_type == other_function_type


@pytest.mark.parametrize(
    "arg_types, result_type",
    [
        ((BaseType("a"), BaseType("b")), BaseType("t")),
        ((BaseType("t"),), BaseType("t")),
        ((BaseType("t"), BaseType("t")), BaseType("t")),
    ],
)
def test_function_type_hash_with_valid_data_returns_valid_hash(
    arg_types: tuple[TypeExpression, ...], result_type: TypeExpression
) -> None:
    """Test equality of function types."""
    function_type = FunctionType(arg_types, result_type)
    other_function_type = FunctionType(arg_types, result_type)
    assert hash(function_type) == hash(other_function_type)


@pytest.mark.parametrize(
    "arg_types, result_type",
    [
        ((BaseType("a"), BaseType("b")), BaseType("t")),
        ((BaseType("t"),), BaseType("t")),
        ((BaseType("t"), BaseType("t")), BaseType("t")),
    ],
)
def test_function_type_arity_with_valid_data_returns_valid_arity(
    arg_types: tuple[TypeExpression, ...], result_type: TypeExpression
) -> None:
    """Test arity of function types."""
    function_type = FunctionType(arg_types, result_type)
    assert function_type.arity == len(arg_types)
