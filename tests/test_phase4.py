"""Tests for Phase 4: Variables, Logic, Loops, Filters, Comments."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import EachBlock, IfBlock, VariableDef
from markup_plus.parser import parse_text
from markup_plus.renderer import (
    to_html,
    evaluate_condition,
    evaluate_iterable,
    apply_filters,
    substitute_variables,
)


# ============================================================
# Variables (parse)
# ============================================================

def test_let_string():
    doc = parse_text('@let name = "Ali"')
    assert doc.variables["name"] == "Ali"


def test_let_number():
    doc = parse_text("@let n = 42")
    assert doc.variables["n"] == 42


def test_let_float():
    doc = parse_text("@let p = 9.5")
    assert doc.variables["p"] == 9.5


def test_let_bool_true():
    doc = parse_text("@let a = true")
    assert doc.variables["a"] is True


def test_let_bool_false():
    doc = parse_text("@let a = false")
    assert doc.variables["a"] is False


def test_let_none():
    doc = parse_text("@let x = none")
    assert doc.variables["x"] is None


def test_let_list_of_numbers():
    doc = parse_text("@let nums = [1, 2, 3]")
    assert doc.variables["nums"] == [1, 2, 3]


def test_let_list_of_strings():
    doc = parse_text('@let names = ["Ali", "Sara"]')
    assert doc.variables["names"] == ["Ali", "Sara"]


def test_let_creates_var_node():
    doc = parse_text('@let x = "y"')
    assert isinstance(doc.children[0], VariableDef)
    assert doc.children[0].name == "x"


# ============================================================
# Variable substitution
# ============================================================

def test_substitute_simple():
    assert substitute_variables("Hi {n}!", {"n": "Ali"}) == "Hi Ali!"


def test_substitute_number():
    assert substitute_variables("{n}", {"n": 42}) == "42"


def test_substitute_undefined_keeps_placeholder():
    assert substitute_variables("{x}", {}) == "{x}"


def test_substitute_with_filter_upper():
    assert substitute_variables("{n|upper}", {"n": "abc"}) == "ABC"


def test_substitute_with_filter_lower():
    assert substitute_variables("{n|lower}", {"n": "ABC"}) == "abc"


def test_substitute_with_filter_length():
    assert substitute_variables("{n|length}", {"n": "hello"}) == "5"


def test_substitute_with_filter_reverse():
    assert substitute_variables("{n|reverse}", {"n": "abc"}) == "cba"


def test_substitute_multiple_filters():
    assert substitute_variables("{n|upper|reverse}", {"n": "abc"}) == "CBA"


# ============================================================
# Condition evaluation
# ============================================================

def test_condition_true_simple():
    assert evaluate_condition("x", {"x": True}) is True


def test_condition_false_simple():
    assert evaluate_condition("x", {"x": False}) is False


def test_condition_eq():
    assert evaluate_condition("x == 5", {"x": 5}) is True
    assert evaluate_condition("x == 5", {"x": 6}) is False


def test_condition_ne():
    assert evaluate_condition("x != 5", {"x": 6}) is True


def test_condition_gt():
    assert evaluate_condition("x > 5", {"x": 10}) is True


def test_condition_lt():
    assert evaluate_condition("x < 5", {"x": 3}) is True


def test_condition_ge():
    assert evaluate_condition("x >= 5", {"x": 5}) is True


def test_condition_le():
    assert evaluate_condition("x <= 5", {"x": 5}) is True


def test_condition_string_eq():
    assert evaluate_condition('role == "admin"', {"role": "admin"}) is True
    assert evaluate_condition('role == "admin"', {"role": "user"}) is False


# ============================================================
# Iterable evaluation
# ============================================================

def test_iterable_from_variable():
    assert evaluate_iterable("items", {"items": [1, 2, 3]}) == [1, 2, 3]


def test_iterable_inline_list():
    assert evaluate_iterable("[1, 2, 3]", {}) == [1, 2, 3]


def test_iterable_inline_strings():
    assert evaluate_iterable('["a", "b"]', {}) == ["a", "b"]


def test_iterable_empty():
    assert evaluate_iterable("x", {"x": []}) == []


# ============================================================
# Filters
# ============================================================

def test_filter_upper():
    assert apply_filters("abc", ["upper"]) == "ABC"


def test_filter_lower():
    assert apply_filters("ABC", ["lower"]) == "abc"


def test_filter_length_string():
    assert apply_filters("hello", ["length"]) == 5


def test_filter_length_list():
    assert apply_filters([1, 2, 3], ["length"]) == 3


def test_filter_reverse_string():
    assert apply_filters("abc", ["reverse"]) == "cba"


def test_filter_reverse_list():
    assert apply_filters([1, 2, 3], ["reverse"]) == [3, 2, 1]


# ============================================================
# Integration — full documents
# ============================================================

def test_document_with_variable():
    src = '@let n = "Ali"\n\n# Hello {n}'
    html = to_html(src)
    assert "Hello Ali" in html


def test_document_with_if_true():
    src = '@let x = 10\n\n@if x > 5\nyes\n@endif'
    html = to_html(src)
    assert "yes" in html


def test_document_with_if_false_else():
    src = '@let x = 3\n\n@if x > 5\nyes\n@else\nno\n@endif'
    html = to_html(src)
    body_start = html.find("<body")
    body = html[body_start:] if body_start != -1 else html
    assert ">no</p>" in body


def test_document_with_elif():
    src = '@let x = 5\n\n@if x > 10\nbig\n@elif x > 3\nmedium\n@else\nsmall\n@endif'
    html = to_html(src)
    assert "medium" in html


def test_document_with_each():
    src = '@let items = ["A", "B", "C"]\n\n@each x in items\n- {x}\n@end'
    html = to_html(src)
    assert "<li>A</li>" in html
    assert "<li>B</li>" in html
    assert "<li>C</li>" in html


def test_document_each_with_index():
    src = '@let items = ["X", "Y"]\n\n@each i, item in items\n{i}: {item}\n@end'
    html = to_html(src)
    assert "0: X" in html
    assert "1: Y" in html


def test_document_if_inside_each():
    src = '''@let nums = [1, 5, 10]

@each n in nums
@if n > 3
big: {n}
@else
small: {n}
@endif
@end'''
    html = to_html(src)
    assert "small: 1" in html
    assert "big: 5" in html
    assert "big: 10" in html


def test_document_with_comment():
    src = '@# this is a comment\n\nvisible text'
    html = to_html(src)
    assert "this is a comment" not in html
    assert "visible text" in html


def test_document_let_does_not_render():
    src = '@let x = 5\n\n# Title'
    html = to_html(src)
    body_start = html.find("<body")
    body = html[body_start:] if body_start != -1 else html
    assert "@let" not in body


def test_document_filter_in_heading():
    src = '@let name = "markup"\n\n# {name|upper}'
    html = to_html(src)
    assert ">MARKUP</h1>" in html


def test_document_variable_in_table():
    src = '@let city = "Tehran"\n\n| Name | City |\n|------|------|\n| Ali  | {city} |'
    html = to_html(src)
    assert "Tehran" in html


def test_document_nested_each():
    src = '''@let groups = [["A", "B"], ["C", "D"]]

@each group in groups
@each item in group
- {item}
@end
@end'''
    html = to_html(src)
    assert "<li>A</li>" in html
    assert "<li>B</li>" in html
    assert "<li>C</li>" in html
    assert "<li>D</li>" in html