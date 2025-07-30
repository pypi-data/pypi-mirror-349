import click
import json
from agentops.core.analyzer import CodeAnalyzer, _add_parents

@click.group()
def cli():
    """AgentOps CLI"""
    pass

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def analyze(file):
    """Analyze a Python file and print structured info."""
    analyzer = CodeAnalyzer()
    # Add parent references for correct function/class extraction
    with open(file, 'r') as f:
        code = f.read()
    import ast
    tree = ast.parse(code)
    _add_parents(tree)
    result = analyzer.analyze_code(code)
    click.echo(json.dumps(result, indent=2, default=str))

if __name__ == '__main__':
    cli() 