import shutil

def create_project(name: str):
    shutil.copytree('../core/project_templates/default', f'./{name}')
