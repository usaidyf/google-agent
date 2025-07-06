import os

def write_file(working_directory, file_path, content):
   try:
      abs_working_directory = os.path.abspath(working_directory)
      # print('abs_working_directory', abs_working_directory)
      
      abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
      # print('abs_file_path', abs_file_path)
      
      if not abs_file_path.startswith(abs_working_directory):
         return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
      if not os.path.exists(abs_file_path):
         os.makedirs(file_path)
      
      with open(abs_file_path, "w") as f:
         f.write(content)
         return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
         
   except Exception as e:
      return f"Error: {e}"