import os
from Importer.data_importer import DataImporter
from Importer.importer_xyz1 import ImporterXYZ1
from Importer.importer_xyz2 import ImporterXYZ2
from Importer.importer_xyz3 import ImporterXYZ3
from Importer.importer_mdb import ImporterMDB

# Specify the directory to search
directory_path = 'test_files'


def find_files_in_first_sublayer(directory):
    all_files = []
    try:
        # Get first-level subdirectories
        subdirs = next(os.walk(directory))[1]  # Get first-level subdirectories
        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            if os.path.isdir(subdir_path):
                for file in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, file)
                    # Ensure it's a file
                    if os.path.isfile(file_path):  
                        all_files.append(file_path)
    except StopIteration:
        print(f"No subdirectories found in {directory}")
    return all_files



if __name__ == "__main__":
    all_files = find_files_in_first_sublayer(directory_path)
    for input_file in all_files : 
    
        data_importer = DataImporter(input_file)
        try:
            data_importer.import_file()
        except ValueError as e:
            print(e)

