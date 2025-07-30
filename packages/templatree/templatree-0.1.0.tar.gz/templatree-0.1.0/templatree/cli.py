
import argparse
import os
import subprocess
from pathlib import Path

def create_structure_from_tree(base_dir, tree_text):
    lines = tree_text.strip().splitlines()
    stack = [base_dir]

    for line in lines:
        stripped = line.lstrip(' │├└─')
        indent_level = (len(line) - len(stripped)) // 4

        while len(stack) > indent_level + 1:
            stack.pop()

        current_dir = stack[-1]
        new_path = current_dir / stripped

        if '.' in stripped:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            new_path.touch()
        else:
            new_path.mkdir(parents=True, exist_ok=True)
            stack.append(new_path)

def create_structure_from_paths(base_dir, path_text):
    lines = path_text.strip().splitlines()
    for line in lines:
        path = Path(line.strip())
        full_path = base_dir / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.touch()

def create_virtualenv(base_dir, venv_name):
    venv_path = base_dir / venv_name
    subprocess.run(["python", "-m", "venv", str(venv_path)])
    print(f"Virtual environment created at: {venv_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate a custom project scaffold.")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a new project structure")
    create_parser.add_argument("project_name", help="Name of the project directory to create")
    create_parser.add_argument(
        "-venv", "--virtualenv",
        help="Optional: Create a Python virtual environment with the given name inside the project"
    )
    create_parser.add_argument(
        "--from-file",
        type=str,
        help="Optional: Load directory structure from a file (.txt) instead of typing it manually"
    )


    args = parser.parse_args()

    if args.command == "create":
        base_dir = Path(args.project_name)
        if base_dir.exists():
            print(f"Error: Directory '{args.project_name}' already exists.")
            return
        base_dir.mkdir()

        if args.from_file:
            structure_path = Path(args.from_file)
            if not structure_path.exists():
                print(f"Error: File '{args.from_file}' not found.")
                return
            with open(structure_path, 'r', encoding='utf-8') as f:
                structure_text = f.read()
            if '├' in structure_text or '│' in structure_text:
                create_structure_from_tree(base_dir, structure_text)
            else:
                create_structure_from_paths(base_dir, structure_text)
        else:
            choice = input("Would you like to send a (1) tree-style template or (2) flat path list? (1 or 2): ").strip()
            print("Enter your structure (end with a line containing only 'EOD'):")

            lines = []
            while True:
                line = input()
                if line.strip() == "EOD":
                    break
                lines.append(line)

            structure_text = "\n".join(lines)

            if choice == "1":
                create_structure_from_tree(base_dir, structure_text)
            elif choice == "2":
                create_structure_from_paths(base_dir, structure_text)
            else:
                print("Invalid choice.")

        if args.virtualenv:
            create_virtualenv(base_dir, args.virtualenv)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
