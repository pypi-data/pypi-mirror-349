from typer import Typer
from necromancer.cli.build_command import build_app

app = Typer()
app.add_typer(build_app)

if __name__ == '__main__':
    app()