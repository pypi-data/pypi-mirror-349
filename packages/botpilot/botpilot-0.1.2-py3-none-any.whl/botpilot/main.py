import typer
from botpilot.commands import init  # <- fully qualified import now

app = typer.Typer(help="Automation CLI for building bot templates.")

app.add_typer(init.app, name="init")

def main():
    app()
