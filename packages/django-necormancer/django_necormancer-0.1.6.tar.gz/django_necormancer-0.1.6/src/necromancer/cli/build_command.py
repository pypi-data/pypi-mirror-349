import typer 
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from rich.progress import Progress, SpinnerColumn, TextColumn

from .utils import create_project, setup_package_manager, setup_build_tools
from .config import CLI_SETTINGS, PACKAGE_MANAGEMENT, ENVIROMENT_SETUP_TOOLS, THIRD_PARTY_PACKAGES

build_app = typer.Typer()

@build_app.command('build')
def cli_build_project():

    name = inquirer.text(
        message="Project name:",
        validate=EmptyInputValidator(),
        **CLI_SETTINGS
    ).execute()

    
    build_tools = inquirer.select(
        message="Select package management tool:",
        choices=PACKAGE_MANAGEMENT,
        default="requirements.txt",
        **CLI_SETTINGS
    ).execute()

    enviroment_setup = inquirer.select(
        message="Select enviroment setup:",
        choices=ENVIROMENT_SETUP_TOOLS,
        default="Make",
        **CLI_SETTINGS
    ).execute()

    install_packages = inquirer.checkbox(
        message="select third party packages:",
        choices=THIRD_PARTY_PACKAGES,
        default="Make",
        **CLI_SETTINGS
    ).execute()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="creating project...", total=None)
        create_project(name)
        setup_package_manager(name, build_tools, install_packages)
        setup_build_tools(name, enviroment_setup)