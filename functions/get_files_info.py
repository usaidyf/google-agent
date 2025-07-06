import os

def get_files_info(working_directory, directory=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        # print('abs_working_directory', abs_working_directory)

        abs_directory = os.path.abspath(os.path.join(working_directory, directory))
        # print('abs_directory', abs_directory)

        list_abs_dir = os.listdir(path=abs_working_directory)
        # print(list_abs_dir)
        
        if directory not in list_abs_dir and directory != ".":
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'

        # print("passed 2 checks...")

        list_dir = os.listdir(path=abs_directory)
        # print(list_dir)

        final_str = ""
        for file in list_dir:
            abs_filepath = os.path.abspath(os.path.join(abs_directory, file))
            file_size = os.path.getsize(abs_filepath)
            is_dir = os.path.isdir(abs_filepath)
            
            final_str += f"- {file}: file_size={file_size} bytes, is_dir={str(is_dir)}\n"

        return final_str

    except Exception as e:
        return f"Error: {e}"
