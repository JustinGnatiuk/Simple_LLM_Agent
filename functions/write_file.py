import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file, relative to the working directory.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    
    abs_working_dir = os.path.abspath(working_directory)

    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(abs_working_dir):

        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    
    if not os.path.exists(full_path):
        try:
            with open(full_path, "x") as file:
                pass
        except Exception as e:
            return f"Error: creating directory: {e}"
    
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:

        with open(full_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path} ({len(content)} characters written)"'

    except Exception as e:

        return f"Error: cannot write to file {file_path} : {e}"

