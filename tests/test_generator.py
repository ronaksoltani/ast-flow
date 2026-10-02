import pytest

from ast_flow.generator import module_to_mermaid


def test_generator_emits_branches_loops_and_functions():
    diagram = module_to_mermaid("def score(items):\n for item in items:\n  if item:\n   return item\n return None\n")
    assert "flowchart TD" in diagram
    assert "Repeat" in diagram and "Yes" in diagram and "Start: score" in diagram


def test_invalid_python_is_reported_as_syntax_error():
    with pytest.raises(SyntaxError):
        module_to_mermaid("def unfinished(:")
