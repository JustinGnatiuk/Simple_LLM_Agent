from google.genai import types
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from config import WORKING_DIR

# List available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# function_call_part is a types.FunctionCall object with .name and .args property
# essentially you can pass a full function name into it
def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # build function dictionary
    function_dict = {
                        "get_file_content": get_file_content,
                        "get_files_info": get_files_info,
                        "run_python_file": run_python_file,
                        "write_file": write_file
                    }

    # return an error type if function doesnt exist
    if function_call_part.name not in function_dict:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

    # add working directory parameter to dictionary of function arguments
    function_args = function_call_part.args
    function_args['working_directory'] = WORKING_DIR

    # call function and store result
    result = function_dict[function_call_part.name](**function_args)

    # return function result type from function call
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )