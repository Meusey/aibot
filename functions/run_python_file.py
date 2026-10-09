import os, subprocess


#block that allows the LLM to run code in a quarantined environment
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot execute "{file_path}" as it is outside '
                f'the permitted working directory'
            )

        if not os.path.isfile(target_file):
            return (
                f'Error:"{file_path}" does not exist'
            )

        if not target_file.endswith(".py"):
            return (
                f'Error:"{file_path}" is not a Python file'
            )

        command = ["python", target_file]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"

            if result.stderr:
                output += f"STDERR:\n{result.stderr}"

        return output

    except Exception as e:
        return f"Error: {str(e)}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional arguments to pass to the Python file.",
                },
            },
            "required": ["file_path"],
        },
    },
}