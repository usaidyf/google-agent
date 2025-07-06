from functions.write_file import write_file

def print_with_red(*args, **kwargs):
   print('\033[31m')
   print(*args, **kwargs)
   print('\033[0m')
      

test_calls = [
   (write_file, "calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
   (write_file, "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
   (write_file, "calculator", "/tmp/temp.txt", "this should not be allowed"),
]

def main():
   for func, param1, param2, param3 in test_calls:
      print_with_red('=====================\n')
      print(func.__name__)
      print('working_directory =', param1)
      print('directory =', param2)
      print('content =', param3)
      print('Results:\n')
      print(func(param1, param2, param3))
      print_with_red('=====================\n')
   
if __name__ == "__main__":
   main()