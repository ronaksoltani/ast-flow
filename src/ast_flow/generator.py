from __future__ import annotations

import ast


def _label(text: str) -> str:
    return " ".join(text.replace("\"", "'").replace("|", "/").replace("[", "(").replace("]", ")").split())[:100]


class _Graph:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.counter = 0
        self.nodes: list[str] = []
        self.edges: list[str] = []

    def node(self, label: str, shape: str = "box") -> str:
        self.counter += 1
        node_id = f"{self.prefix}_{self.counter}"
        if shape == "diamond":
            self.nodes.append(f'    {node_id}{{"{_label(label)}"}}')
        elif shape == "round":
            self.nodes.append(f'    {node_id}(["{_label(label)}"])')
        else:
            self.nodes.append(f'    {node_id}["{_label(label)}"]')
        return node_id

    def connect(self, sources: list[str], target: str, label: str = "") -> None:
        suffix = f"|{label}|" if label else ""
        self.edges.extend(f"    {source} -->{suffix} {target}" for source in sources)

    def block(self, statements: list[ast.stmt], incoming: list[str]) -> list[str]:
        frontier = incoming
        for statement in statements:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(statement, ast.If):
                decision = self.node(f"if {ast.unparse(statement.test)}", "diamond")
                self.connect(frontier, decision)
                yes, no = self.node("yes", "round"), self.node("no", "round")
                yes_stops = self.block(statement.body, [yes])
                no_stops = self.block(statement.orelse, [no]) if statement.orelse else [no]
                self.connect([decision], yes, "Yes")
                self.connect([decision], no, "No")
                frontier = yes_stops + no_stops
                continue
            if isinstance(statement, (ast.For, ast.AsyncFor, ast.While)):
                condition = (f"for {ast.unparse(statement.target)} in {ast.unparse(statement.iter)}"
                             if isinstance(statement, (ast.For, ast.AsyncFor))
                             else f"while {ast.unparse(statement.test)}")
                decision = self.node(condition, "diamond")
                self.connect(frontier, decision)
                body = self.node("loop body", "round")
                after = self.node("done", "round")
                self.connect([decision], body, "Repeat")
                self.connect([decision], after, "Exit")
                body_stops = self.block(statement.body, [body])
                self.connect(body_stops, decision)
                frontier = [after]
                continue
            label = ast.unparse(statement)
            shape = "round" if isinstance(statement, ast.Return) else "box"
            node = self.node(label, shape)
            self.connect(frontier, node)
            if isinstance(statement, (ast.Return, ast.Raise)):
                frontier = []
            else:
                frontier = [node]
        return frontier


def module_to_mermaid(source: str) -> str:
    """Parse Python and return a Mermaid flowchart without executing it."""
    tree = ast.parse(source)
    sections: list[str] = ["flowchart TD"]
    definitions: list[tuple[str, list[ast.stmt]]] = []
    module_body = [node for node in tree.body if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    if module_body:
        definitions.append(("module", module_body))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            definitions.append((node.name, node.body))
    for index, (name, body) in enumerate(definitions, start=1):
        graph = _Graph(f"g{index}")
        start = graph.node(f"Start: {name}", "round")
        end = graph.node("End", "round")
        frontier = graph.block(body, [start])
        graph.connect(frontier, end)
        sections.extend([f'  subgraph graph_{index}["{_label(name)}"]', *graph.nodes, *graph.edges, "  end"])
    return "\n".join(sections) + "\n"
