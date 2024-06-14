import os
import shutil
from datetime import datetime

def get_sorting_criterion():
    print("Based on what criterion would you like to sort the files?")
    print("1. Extension")
    print("2. Date")
    print("3. Year")
    print("4. File size")
    criterion = input("Please enter the number of your choice: ")
    return criterion

def sort_files(user_path, criterion):
    for root, dirs, files in os.walk(user_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            if criterion == "1":  # Extension
                ext = os.path.splitext(name)[1][1:].upper()
                target_folder = os.path.join(user_path, ext)
            elif criterion == "2":  # Date
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
                target_folder = os.path.join(user_path, file_date)
            elif criterion == "3":  # Year
                file_year = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y')
                target_folder = os.path.join(user_path, file_year)
            elif criterion == "4":  # File size
                size = os.path.getsize(file_path)
                if size < 1024 * 1024:  # less than 1MB
                    size_folder = "Small files"
                elif size < 1024 * 1024 * 100:  # less than 100MB
                    size_folder = "Medium files"
                else:
                    size_folder = "Large files"
                target_folder = os.path.join(user_path, size_folder)
            else:
                print("Invalid criterion.")
                return

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            shutil.move(file_path, os.path.join(target_folder, name))

if __name__ == "__main__":
    user_path = input("Please enter the path where the files are located: ")
    criterion = get_sorting_criterion()
    sort_files(user_path, criterion)
    print("Files have been sorted.")
