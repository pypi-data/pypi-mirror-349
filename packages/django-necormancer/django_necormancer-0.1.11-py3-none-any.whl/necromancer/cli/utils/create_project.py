import shutil
from necromancer.cli.config import BASE_DIR
import os



def create_project(name: str):
    full_path = os.path.join(BASE_DIR, 'core/project_templates/default')
    shutil.copytree(full_path, f'./{name}')
