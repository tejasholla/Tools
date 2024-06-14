import os
from datetime import datetime

def rename_files(directory, action, pattern="%Y%m%d%H%M%S", text_to_remove="", recursive=False, file_types=None, preview=False):
    changes = []
    for root, dirs, files in os.walk(directory):
        if file_types:
            files = [f for f in files if os.path.splitext(f)[1].lower() in file_types]

        for filename in files:
            file_path = os.path.join(root, filename)
            if action == "rename":
                new_filename = datetime.now().strftime(pattern) + "_" + filename
            elif action == "delete":
                new_filename = filename.replace(text_to_remove, "")
            new_file_path = os.path.join(root, new_filename)

            if preview:
                print(f"Preview: '{file_path}' will be renamed to '{new_file_path}'")
                changes.append((file_path, new_file_path))
            else:
                os.rename(file_path, new_file_path)
                print(f"Renamed '{file_path}' to '{new_file_path}'")

        if not recursive:
            break

    # After showing preview, ask if user wants to proceed
    if preview:
        proceed = input("Do you want to proceed with these changes? (yes/no): ").strip().lower()
        if proceed == "yes":
            for old_path, new_path in changes:
                os.rename(old_path, new_path)
                print(f"Renamed '{old_path}' to '{new_path}'")
        else:
            print("No changes were made.")

def get_user_input():
    directory = input("Enter the directory path to process: ").strip()
    action = input("Do you want to 'rename' or 'delete' part of the filenames? (rename/delete): ").strip().lower()
    
    pattern, text_to_remove = "%Y%m%d%H%M%S", ""
    if action == "rename":
        pattern = input("Enter the pattern for renaming files (leave blank for default timestamp): ").strip() or "%Y%m%d%H%M%S"
    elif action == "delete":
        text_to_remove = input("Enter the text to remove from filenames: ").strip()

    recursive = input("Rename files in subdirectories recursively? (yes/no): ").strip().lower() == "yes"
    types = input("Enter a comma-separated list of file extensions to include (leave blank for all files): ").strip()
    file_types = {f".{ext.strip().lower()}" for ext in types.split(",")} if types else None
    preview = input("Would you like to preview the changes before renaming? (yes/no): ").strip().lower() == "yes"
    
    return directory, action, pattern, text_to_remove, recursive, file_types, preview

def main():
    directory, action, pattern, text_to_remove, recursive, file_types, preview = get_user_input()
    
    if not os.path.isdir(directory):
        print("The specified directory does not exist. Please check the path and try again.")
        return
    
    # Adjusted call to incorporate preview logic within the function itself
    rename_files(directory, action, pattern, text_to_remove, recursive, file_types, preview)

if __name__ == "__main__":
    main()