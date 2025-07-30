import shutil
import subprocess
from subprocess import DEVNULL
import venv
import tempfile
from pathlib import Path
from necromancer.cli.config import THIRD_PARTY_DEV_PACKAGES, THIRD_PARTY_PROD_PACKAGES
from necromancer.cli.config import BASE_DIR
import os

def add_packages(name, packages):
    base_requirements_path = f'./{name}/requirements'

    for package in packages:
        requirements_path = base_requirements_path

        if package in THIRD_PARTY_DEV_PACKAGES:
            requirements_path += '/dev.in'
        elif package in THIRD_PARTY_PROD_PACKAGES:
            requirements_path += '/prod.in'
        else:
            requirements_path += '/base.in'

        with open(requirements_path, '+a') as file:
            file.write(f'{package}\n')

def setup_package_manager(name: str, package_management_tool: str, packages: list[str]):

    if package_management_tool == 'pip-tools':
        with tempfile.TemporaryDirectory() as temp_directory:
            temp_directory_path = Path(temp_directory)

            venv.EnvBuilder(with_pip=True).create(temp_directory_path)
            full_path = os.path.join(BASE_DIR, 'core/requirements/pip-tools')

            shutil.copytree(full_path, f'./{name}/requirements')
            add_packages(name, packages)
            subprocess.run(
                ['pip', 'install', 'pip-tools'],
                stdout=DEVNULL,
                stderr=DEVNULL
            )

            subprocess.run(
                ['pip-compile', '-o', f'./{name}/requirements/requirements-dev.txt', f'./{name}/requirements/dev.in'],
                stdout=DEVNULL,
                stderr=DEVNULL
            )


