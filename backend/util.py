import os

def count_lines_of_code(file_path):
    """
    Counts the total number of lines of code in a file.

    Args:
        file_path: The path to the file.

    Returns:
        The total number of lines of code in the file.
    """

    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Count the number of lines that are not empty or comments
    code_lines = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            code_lines += 1

    return code_lines

cnt = 0
cnt += count_lines_of_code("app.py")
cnt += count_lines_of_code("init.py")
cnt += count_lines_of_code("test_user_management.py")
cnt += count_lines_of_code("user_management.py")
cnt += count_lines_of_code("util.py")
print(cnt) # 390