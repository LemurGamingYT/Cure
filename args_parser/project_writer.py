from pathlib import Path
from json import dumps
from sys import argv


def is_project(path: Path) -> bool:
    return path.is_dir() and (path / 'project.json').exists() and (path / 'src').is_dir()

def ask_user(prompt: str, choices: set[str], nudge_message: str) -> str:
    user = ''
    while user not in choices:
        user = input(prompt)
        if user not in choices:
            print(nudge_message)
    
    return user

def cli_project_create() -> tuple[bool, str]:
    if len(argv) <= 2:
        return False, 'Usage: cure init [project name]'
    
    project_name = argv[2]
    path = Path.cwd() / project_name
    if path.is_file():
        return False, f'{path} is a file'
    
    if path.is_dir() and len(list(path.iterdir())) > 0:
        should_continue = ask_user(
            f'{path} is not empty. Do you still want to create the project (y/n): ',
            {'y', 'n'}, 'Please enter y (for yes) or n (for no)'
        )
        if should_continue == 'n':
            return True, ''
    
    return make_project(project_name, path)

def make_project(name: str, folder: Path) -> tuple[bool, str]:
    folder.mkdir(parents=True, exist_ok=True)
    
    src_folder = folder / 'src'
    src_folder.mkdir(parents=True, exist_ok=True)
    
    main_file = src_folder / 'main.cure'
    main_file.write_text("""func main() -> int {
    return 0
}
""")
    
    json = folder / 'project.json'
    json.write_text(dumps({
        'name': name,
        'main-file': main_file.as_posix()
    }, indent=4))
    
    return True, ''
