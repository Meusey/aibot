from functions.get_file_content import get_file_content


#bootdev test for the get_file_content function and debugging
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat")) #this should return an error string
print(get_file_content("calculator", "pkg/does_not_exist.py")) #this should return an error string

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")