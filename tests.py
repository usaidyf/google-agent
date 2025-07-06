from functions.run_python_file import run_python_file

def print_with_red(*args, **kwargs):
   print('\033[31m')
   print(*args, **kwargs)
   print('\033[0m')
      

test_calls = [
   (run_python_file, "calculator", "main.py"),
   (run_python_file, "calculator", "tests.py"),
   (run_python_file, "calculator", "../main.py"),
   (run_python_file, "calculator", "nonexistent.py"),
]

def main():
   for func, param1, param2 in test_calls:
      print_with_red('=====================\n')
      print(func.__name__)
      print('working_directory =', param1)
      print('file_path =', param2)
      print('Results:\n')
      print(func(param1, param2))
      print_with_red('=====================\n')
   
if __name__ == "__main__":
   main()