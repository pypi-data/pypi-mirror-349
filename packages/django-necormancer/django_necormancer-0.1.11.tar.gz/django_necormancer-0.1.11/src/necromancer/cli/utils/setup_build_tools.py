import shutil
from necromancer.cli.config import BASE_DIR
import os

def setup_build_tools(project_name: str, selected_build_tool: str):
    full_path = os.path.join(BASE_DIR, 'core/build_tools/Make/Makefile')

    if selected_build_tool == 'Make':
        shutil.copyfile(full_path, f'./{project_name}/Makefile')
