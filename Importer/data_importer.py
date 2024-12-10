import os
from Importer.importer_xyz1 import ImporterXYZ1
from Importer.importer_xyz2 import ImporterXYZ2
from Importer.importer_xyz3 import ImporterXYZ3
from Importer.importer_mdb import ImporterMDB

# This will choose which importer to use according to the file we have

class DataImporter:
    def __init__(self, input_file):
        self.input_file = input_file
        self.base_name = os.path.splitext(os.path.basename(input_file))[0]

    def get_xyz_importer(self):
        with open(self.input_file, 'r') as file:
            first_line = file.readline().strip()
        
        if first_line.startswith('B'):
            return ImporterXYZ1
        elif first_line.startswith('T'):
            return ImporterXYZ2
        elif first_line.startswith('['):
            return ImporterXYZ3
        else :
            raise ValueError("Required xyz file does not have his own importer.")


    def get_importer(self):
        # Get the file extension without the dot
        file_extension = os.path.splitext(self.input_file)[1][1:]  
        if file_extension == 'xyz' :
            return self.get_xyz_importer()
        if file_extension == 'mdb' :
            return ImporterMDB
        else : 
            raise ValueError("Unknown extension.")


    def import_file(self):
        importer_class = self.get_importer()
        output_file = os.path.join("results")
        # Instantiate the importer class with required arguments
        importer_instance = importer_class(self.input_file, output_file)  
        # Call the import method on the instance
        importer_instance.import_data()  

