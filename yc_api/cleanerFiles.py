import os
import shutil

# Define the list of directories and files to clean
dirs_to_clean = [
    '__pycache__',  # Python cache files
    'migrations'    # Migration files
]
files_to_clean = [
    'db.sqlite3'    # SQLite database file
]

# Recursively remove all __pycache__ and migration files
def remove_dirs(root_dir, dirs):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname in dirs:
                dir_to_remove = os.path.join(dirpath, dirname)
                print(f"Removing directory: {dir_to_remove}")
                shutil.rmtree(dir_to_remove, ignore_errors=True)
                
                # Recreate the migrations folder with an empty __init__.py
                if dirname == 'migrations':
                    migrations_path = os.path.join(dirpath, 'migrations')
                    os.makedirs(migrations_path, exist_ok=True)
                    init_file = os.path.join(migrations_path, '__init__.py')
                    open(init_file, 'w').close()  # Create an empty __init__.py file
                    print(f"Recreated migrations folder: {migrations_path} with __init__.py")

# Remove specific files like db.sqlite3
def remove_files(root_dir, files):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file in files:
                file_to_remove = os.path.join(dirpath, file)
                print(f"Removing file: {file_to_remove}")
                os.remove(file_to_remove)

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Remove cache and migration directories
    remove_dirs(project_root, dirs_to_clean)

    # Remove specific files like db.sqlite3
    remove_files(project_root, files_to_clean)

    print("Cleaned Django project successfully!")
