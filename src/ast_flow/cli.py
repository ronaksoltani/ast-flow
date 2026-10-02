import argparse
from pathlib import Path

from .generator import module_to_mermaid


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert Python control flow to Mermaid.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("flowchart.mmd"))
    args = parser.parse_args(argv)
    try:
        diagram = module_to_mermaid(args.source.read_text(encoding="utf-8"))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(diagram, encoding="utf-8")
    except (OSError, SyntaxError, ValueError) as error:
        parser.error(str(error))
    print(f"Wrote Mermaid flowchart to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
