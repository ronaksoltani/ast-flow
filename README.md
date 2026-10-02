# Python AST Flow

Turn Python source into a Mermaid flowchart using Python's built-in abstract syntax tree. The generator models function bodies, branches, loops, returns, and ordinary statements without executing the input program.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
ast-flow src/app.py --output docs/app-flow.mmd
```

Paste the generated Mermaid into a Markdown file or a Mermaid-compatible viewer. This is a structural learning aid: dynamic dispatch, exceptions, decorators, and runtime behavior are not fully represented.

## Learning notes

`ast.parse` turns source text into typed nodes such as `FunctionDef`, `If`, and `For`. The builder assigns stable node IDs and emits Mermaid edges. Reading the input is safe; generated labels are escaped so punctuation cannot accidentally become Mermaid syntax.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
