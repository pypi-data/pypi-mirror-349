import pytest
from string_list import list_from_string, string_from_list, list_from_any, case_insensitive_update, str_enumerate


def test_list_from_string():
    assert list_from_string("a,b,c") == ["a", "b", "c"]
    assert list_from_string(" a , b , c ", strip=True) == ["a", "b", "c"]
    assert list_from_string("x|y|z", delim="|") == ["x", "y", "z"]


def test_string_from_list():
    assert string_from_list(["a", "b", "c"]) == "a,b,c"
    assert string_from_list(["a", "b"], quoted=True) == "'a','b'"


def test_list_from_any():
    assert list_from_any("1,2,3", return_items_as_int=True) == [1, 2, 3]
    assert list_from_any(["a", "b"]) == ["a", "b"]
    assert list_from_any(123) == ["123"]


def test_case_insensitive_update():
    existing = {"Film", "Movie"}
    new = {"film", "Cinema"}
    result = case_insensitive_update(existing, new)
    assert "Film" in result
    assert "Movie" in result
    assert "Cinema" in result
    assert "film" not in result


def test_str_enumerate():
    result = str_enumerate("apple,banana", start=1)
    assert result == {"1": "apple", "2": "banana"}
