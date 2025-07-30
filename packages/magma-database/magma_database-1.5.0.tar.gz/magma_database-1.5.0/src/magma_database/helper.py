import os
from importlib_resources import files
import datetime
import shutil


def copy_env(overwrite: bool = False) -> None:
    """Copy .env.local example to working directory.

    Args:
        overwrite (bool, optional): Whether to overwrite existing files. Defaults to False.

    Returns:
        None
    """
    source_env_file = str(files("magma_database.resources").joinpath(".env.local.example"))
    destination_env_file = os.path.join(os.getcwd(), "env.local.example")

    if os.path.exists(destination_env_file) and not overwrite:
        print(f"{destination_env_file} already exists, skipping. Use overwrite=True to overwrite.")
        return None

    try:
        # Backup existing env file
        local_env = os.path.join(os.getcwd(), ".env.local")
        if os.path.exists(local_env):
            current_datetime = datetime.datetime.now()
            print(f"[{current_datetime}] Backup {local_env} to .env.local.bak")
            shutil.copy(local_env, os.path.join(os.getcwd(), "env.local.bak"))

        if os.path.exists(destination_env_file) and overwrite:
            os.remove(destination_env_file)

        shutil.copy(source_env_file, destination_env_file)
        current_datetime = datetime.datetime.now()
        print(f"[{current_datetime}] Env file: .env.local.example copied to {destination_env_file}")
        return None
    except PermissionError:
        print("❌ Permission denied.")
        return None
