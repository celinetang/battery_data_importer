import os
import pandas as pd

# This is the parent Class from which 4 different importer classes will inherit

class BaseImporter :
    def __init__(self, input_file, output_dir='results'):
        self.input_file = input_file
        self.output_dir = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0])
        self.base_name = os.path.splitext(os.path.basename(input_file))[0]
        self.metadata = {}

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_metadata(self):
        raise NotImplementedError

    def import_data(self):
        raise NotImplementedError

    def save_metadata(self):
        meta_file = os.path.join(self.output_dir, f"{self.base_name}_metadata.txt")
        with open(meta_file, 'w') as file:
            for key, value in self.metadata.items():
                if isinstance(value, dict):
                    file.write(f"[{key}]\n")
                    for subkey, subvalue in value.items():
                        file.write(f"{subkey}: {subvalue}\n")
                else:
                    file.write(f"{key}: {value}\n")

    def save_data_as_csv(self, data):
        csv_file = os.path.join(self.output_dir, f"{self.base_name}.csv")
        data.to_csv(csv_file, index=False)

        
    

    

    
