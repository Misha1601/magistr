import os

def create_txt_file():
    # Get the current directory
    current_dir = os.getcwd()

    # Create the file path
    file_path = os.path.join(current_dir, 'hello_world.txt')

    # Open the file
    with open(file_path, 'w') as f:
        # Write the text
        f.write('Hello World!')

# Call the function
create_txt_file()