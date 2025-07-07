import os
import subprocess
from subprocess import CalledProcessError
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
   name="run_python_file",
   description="(Use with caution and surety) Run a Python file. This function tries to run a Python file and if successful, returns an output containing stdout, stderr and also an exit code field if the run file try exits with a non-zero code. If a file is not a Python file it returns an error. If no output is produced it returns exactly 'No output produced.'. Also handles other exceptions, if occurs, and returns them as 'Error: {exception}'",
   parameters=types.Schema(
      type=types.Type.OBJECT,
      properties={
         "file_path": types.Schema(
            type=types.Type.STRING,
            description="The file_path parameter, could include slashes too but must be inside the working directory (the working directory although is hard coded in the code). This parameter specifies which python file to run"
         )
      }
   )
)

def run_python_file(working_directory, file_path):
   try:
      abs_working_directory = os.path.abspath(working_directory)
      # print('abs_working_directory', abs_working_directory)

      abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
      # print('abs_file_path', abs_file_path)

      if not abs_file_path.startswith(abs_working_directory):
         return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
      if not os.path.isfile(abs_file_path):
         return f'Error: File "{file_path}" not found.'
      if file_path[-3:] != '.py':
         return f'Error: "{file_path}" is not a Python file.'

      print(f'Trying to run {file_path} file...')

      final_output = ""
      try:
         subprocess_run = subprocess.run(['python3', abs_file_path], timeout=30, capture_output=True, check=True)
         final_output += f"STDOUT: {subprocess_run.stdout}\n"
         final_output += f"STDERR: {subprocess_run.stderr}\n"
         if subprocess_run.stdout is None or subprocess_run.stdout == "":
            return "No output produced."
      except CalledProcessError as e:
         final_output += f"Process exited with code {e.returncode}\n"
      except Exception as e:
         return f"Error: executing Python file: {e}"
      
      return final_output
      
   except Exception as e:
      return f"Error: {e}"
