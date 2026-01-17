import os


def delete_pyc_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")


if __name__ == "__main__":
    school_management = "."  # Change this to your desired directory
    delete_pyc_files(school_management)
