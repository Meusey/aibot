from functions.get_files_info import get_files_info

#bootdev test for the get_files_info function and debugging
print("Result for current directory:\n")
print(get_files_info("calculator", "."))
print("Result for '/bin' directory:\n")
print(get_files_info("calculator", "/bin"))
print("Result for '../' directory:\n")
print(get_files_info("calculator", "../"))
print("Result for 'pkg' directory:\n")
print(get_files_info("calculator", "pkg"))
