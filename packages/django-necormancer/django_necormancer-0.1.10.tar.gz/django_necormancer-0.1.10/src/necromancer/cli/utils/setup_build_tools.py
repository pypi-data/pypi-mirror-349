import shutil

def setup_build_tools(project_name: str, selected_build_tool: str):
    
    if selected_build_tool == 'Make':
        shutil.copyfile('../core/build_tools/Make/Makefile', f'./{project_name}/Makefile')
