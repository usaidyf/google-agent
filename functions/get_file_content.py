import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
   try:
      abs_working_directory = os.path.abspath(working_directory)
      # print('abs_working_directory', abs_working_directory)

      abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
      # print('abs_file_path', abs_file_path)

      if not abs_file_path.startswith(abs_working_directory):
         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
      if not os.path.isfile(abs_file_path):
         return f'Error: File not found or is not a regular file: "{file_path}"'

      with open(abs_file_path, "r") as f:
         file_contents = f.read(MAX_CHARS)
         if file_contents == MAX_CHARS:
               file_contents += (
                  f'[...File "{file_path}" truncated at 10000 characters]'
               )
         return file_contents

   except Exception as e:
      return f"Error: {e}"
