import subprocess
import os
import pandas as pd
from Importer.base_importer import BaseImporter

class ImporterMDB(BaseImporter) :
    def __init__(self, input_file, output_dir='results'):
        super().__init__(input_file, output_dir)
        self.extracted_data_dir = os.path.join(self.output_dir, "extracted_data")
        
      
    # Function to list all tables in the MDB file
    def list_tables(self):
        result = subprocess.run(['mdb-tables', self.input_file], capture_output=True, text=True)
        tables = result.stdout.strip().split()
        return tables

    # Function to export a table to a CSV file
    def export_table_to_csv(self, table_name):
        csv_file_path = os.path.join(self.extracted_data_dir, f"{table_name}.csv")
        with open(csv_file_path, 'w') as csv_file:
            subprocess.run(['mdb-export', self.input_file, table_name], stdout=csv_file)

    # Main function to export all tables to CSV files
    def export_all_tables(self):
        if not os.path.exists(self.extracted_data_dir):
            os.makedirs(self.extracted_data_dir)

        tables = self.list_tables()
        for table in tables:
            self.export_table_to_csv(table)
            



    def extract_metadata(self):
        # Assuming the metadata file is named 'Test.csv' and located in the output directory
        metadata_path = os.path.join(self.extracted_data_dir, 'Test.csv')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as file:
                for line in file:
                    if line.strip() == "":
                        break
                    if ":" in line:
                        key, value = line.split(":", 1)
                        self.metadata[key.strip()] = value.strip()
        else:
            print("Metadata file 'Test.csv' not found in the output directory.")


    def import_data(self):
        # Extract the tables from the mdb file
        self.export_all_tables()

        # Extract and save the metadata
        self.extract_metadata()
        self.save_metadata()

        # The units and variables are not in the same tables
        # Extract the units from Variables.csv
        units = pd.read_csv(os.path.join(self.extracted_data_dir, 'Variables.csv'))
        # Creating a dictionary to map variables to units
        unit_mapping = dict(zip(units['FieldName'], units['AbbrvUnits']))
        
        # Load data
        df = pd.read_csv(os.path.join(self.extracted_data_dir, 'Data_sG.csv'))
    
        # Define column mappings for column normalization
        new_columns = [f"{col} [{unit_mapping.get(col, 'Unknown Unit')}]" for col in df.columns]
        df.columns = new_columns
        column_mapping_mdb = {
                'Total Time [S]': 'Testing_Time [s]',
                    }
        df.rename(columns=column_mapping_mdb, inplace=True)
        
        self.save_data_as_csv(df)
        



