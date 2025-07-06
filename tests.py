from functions.get_files_info import get_files_info

def print_with_red(*args, **kwargs):
   print('\033[31m')
   print(*args, **kwargs)
   print('\033[0m')
      

test_calls = [
   (get_files_info, "calculator", "."),
   (get_files_info, "calculator", "pkg"),
   (get_files_info, "calculator", "/bin"),
   (get_files_info, "calculator", "../"),
]

def main():
   for func, param1, param2 in test_calls:
      print_with_red('=====================\n')
      print(func.__name__)
      print('working_directory =', param1)
      print('directory =', param2)
      print('Results:\n')
      print(func(param1, param2))
      print_with_red('=====================\n')
   
if __name__ == "__main__":
   main()