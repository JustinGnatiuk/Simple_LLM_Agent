import os

def get_files_info(working_directory, directory=None):
    
    try:
        full_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), directory))

        # validate that the given directory is within the permitted working directory
        if full_path.startswith(os.path.abspath(working_directory)):

            # validate directory exists
            if os.path.isdir(full_path):

                content_list = os.listdir(full_path)
                content_string = ""

                print(f"validating directory: {full_path}.....")
                print(f"validating content: {content_list}...")

                for item in content_list:

                    print(f"Checking item: {os.path.join(full_path, item)}")
                    path_to_item = os.path.join(full_path, item)
                    content_string += f"- {item}: file_size={os.path.getsize(path_to_item)} bytes, is_dir={os.path.isdir(path_to_item)}\n"

                return content_string

            else:
                return f'Error: "{directory}" is not a directory'

        else:
            return f'Error: Cannot list "{directory}" as it is outside of the permitted working directory'
    
    except FileNotFoundError:
        return "Error: File not found"
    
    except Exception as e:
        return f"Error: {e}"
