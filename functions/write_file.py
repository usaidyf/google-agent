import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
   name="write_file",
   description="Write to a file specified with the file_path with the content parameter, constrained to the working directory. This function overwrites the existing content of the file at the specified file_path.",
   parameters=types.Schema(
      type=types.Type.OBJECT,
      properties={
         "file_path": types.Schema(
            type=types.Type.STRING,
            description="The file_path parameter, could include slashes too but must be inside the working directory (the working directory although is hard coded in the code)"
         ),
         "content": types.Schema(
            type=types.Type.STRING,
            description="The content to be added to the specified file_path"
         )
      }
   )
)

def write_file(working_directory, file_path, content):
   try:
      abs_working_directory = os.path.abspath(working_directory)
      # print('abs_working_directory', abs_working_directory)
      
      abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
      print('abs_file_path', abs_file_path)
      
      if not abs_file_path.startswith(abs_working_directory):
         return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
      if not os.path.exists(os.path.dirname(abs_file_path)):
         os.makedirs(file_path)
      
      with open(abs_file_path, "w") as f:
         f.write(content)
         return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
         
   except Exception as e:
      return f"Error: {e}"