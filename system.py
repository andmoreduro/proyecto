from subprocess import DEVNULL, Popen
from typing import Optional


def write_to_file(file_path: str, content: str):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file: {e}")


def run_command(command: list[str], stdout_file_path: Optional[str] = None, stderr_file_path: Optional[str] = None) -> Optional[Popen]:
    try:
        stdout_handle = None
        stderr_handle = None
        if stdout_file_path:
            try:
                stdout_handle = open(stdout_file_path, "ab")
            except FileNotFoundError:
                print(f"File \"{stdout_file_path}\" not found.")
                return None
        if stderr_file_path:
            if stderr_file_path == stdout_file_path:
                stderr_handle = stdout_handle
            else:
                try:
                    stderr_handle = open(stderr_file_path, "ab")
                except FileNotFoundError:
                    print(f"File \"{stderr_file_path}\" not found.")
                    return None
        process = Popen(
            command,
            stdin = DEVNULL,
            stdout = stdout_handle if stdout_handle else DEVNULL,
            stderr = stderr_handle if stderr_handle else DEVNULL,
        )
        return process
    except Exception as e:
        print(f"Error running command: {e}")
        return None
