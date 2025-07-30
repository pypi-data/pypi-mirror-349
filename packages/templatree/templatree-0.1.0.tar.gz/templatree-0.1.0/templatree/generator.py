import os
import shutil
from pathlib import Path

def copy_template(destination: str):
    base_path = Path(__file__).parent / "templates"
    destination_path = Path(destination)

    if destination_path.exists():
        raise FileExistsError(f"Destination '{destination}' already exists.")

    shutil.copytree(base_path, destination_path)
    print(f"Project created at: {destination}")
