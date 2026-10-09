import os

MAX_CHARS = 10000


#block that defines the get_file_content function for reading file contents with a maximum of 10000 MAX_CHARS characters
def get_file_content(working_directory: str, file_path: str) -> str:
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
                f'Error: Cannot read "{file_path}" as it is outside '
                f"the permitted working directory"
            )

        if not os.path.isfile(target_file):
            return (
                f'Error: File not found or is not a regular file: "{file_path}"'
            )

        with open(target_file, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at '
                    f"{MAX_CHARS} characters]"
                )

        return file_content_string

    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file, up to a maximum of 10,000 characters.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}