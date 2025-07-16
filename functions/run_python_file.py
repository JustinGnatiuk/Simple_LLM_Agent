import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file within working directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to execute, relative to the working directory.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path):

    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:

        result = subprocess.run(
            ["python3", full_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            cwd=os.path.abspath(working_directory),
            text=True, 
            timeout=30
            )


        return_string = ''

        if not result.returncode == 0:
            return_string += f'Process exited with code {result.returncode}\n'
        if not result.stdout == '':
                return_string += f'STDOUT: {result.stdout}\n'
        if not result.stderr == '':
                return_string += f'STDERR: {result.stderr}\n'
        if return_string == '':
                return f'No output produced.'
                

        return f'{return_string}'
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

    