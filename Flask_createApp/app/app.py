import os
import shutil
def main():
    name = input("Enter the name of the folder: ")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(BASE_DIR, "templates")
    templates = os.listdir(templates_path)
    for i, folder in enumerate(templates):
        print(f"{i+1}. {folder}")
    copy = int(input("Enter the number of what to copy"))
    source_folder = os.path.join(templates_path, templates[copy-1])
    destination_parent = os.getcwd()
    new_folder_name = name

    destination_folder = os.path.join(destination_parent, new_folder_name)

    shutil.copytree(source_folder, destination_folder)

if __name__ == "__main__":
    main()