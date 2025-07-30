import argparse
from .utils import Command, KannaConfig, load_config_from_project
import subprocess

def build_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "Kanna is a task runner for pyproject environments."
    )
    parser.add_argument("task", nargs="?", help="Task identifier defined on tool.kanna.tasks")
    parser.add_argument("--list", "-l", action="store_true", help="List all available tasks that kanna can run")
    return parser.parse_args()

def get_command(identifier: str, config: KannaConfig) -> Command:
    command: Command | None = config.get('tasks').get(identifier)

    if command is None:
        raise RuntimeError(f"The {identifier} task was not defined on pyproject")

    return command

def run_task(identifier: str, config: KannaConfig) -> None:

    command = get_command(identifier=identifier, config=config)

    if isinstance(command, str):
        subprocess.run(command, shell=True, check=True)
        return
    
    pre_commands = command.get('pre', []) or []
    post_commands = command.get('post', []) or []

    for pre in pre_commands:
        run_task(pre, config)
    
    subprocess.run(command.get('command', ''), shell=True, check=True)

    for post in post_commands:
        run_task(post, config)

def run() -> None:
    args = build_argparse()
    config = load_config_from_project()

    if args.list:
        rows: list[tuple[str, str]] = []

        for name, task in config.get('tasks', {}).items():
            help_txt: str = ""

            if not isinstance(task, str):
                help_txt = task.get('help') or ""

            rows.append((name, help_txt))

        if not rows:
            return

        name_width = max(len("Task"), max(len(row[0]) for row in rows))
        desc_width = max(len("Description"), max(len(row[1]) for row in rows))

        # Print header
        print(f"{'Task':<{name_width}}  {'Description':<{desc_width}}")
        print(f"{'-' * name_width}  {'-' * desc_width}")

        # Print rows
        for name, description in rows:
            print(f"{name:<{name_width}}  {description:<{desc_width}}")

        return

    run_task(args.task, config)