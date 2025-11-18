import pytest

from nslps.formal_language.fundamentals.types import BaseType


@pytest.mark.parametrize(
    "name",
    [
        "t",
        "T",
        "Type_1",
    ],
)
def test_base_type_creation_with_valid_name_returns_base_type(name: str) -> None:
    """Test creation of base type with a valid name."""
    base_type = BaseType(name)
    assert base_type.name == name


@pytest.mark.parametrize(
    "name",
    [
        "t",
        "T",
        "Type_1",
    ],
)
def test_base_type_equality_with_valid_data_returns_true(name: str) -> None:
    """Test equality of base types."""
    base_type = BaseType(name)
    other_base_type = BaseType(name)
    assert base_type == other_base_type


@pytest.mark.parametrize(
    "name",
    [
        "t",
        "T",
        "Type_1",
    ],
)
def test_base_type_hash_with_valid_data_returns_valid_hash(name: str) -> None:
    """Test equality of base types hashes."""
    base_type = BaseType(name)
    other_base_type = BaseType(name)
    assert hash(base_type) == hash(other_base_type)
