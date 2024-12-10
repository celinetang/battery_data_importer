import pandas as pd
from Importer.base_importer import BaseImporter

class ImporterXYZ1(BaseImporter) :
    def __init__(self, input_file, output_dir='results'):
        super().__init__(input_file, output_dir)
    
    def extract_metadata(self):
        with open(self.input_file, 'r') as file:
            for line in file:
                if line.strip() == "":
                    break
                if ":" in line:
                    key, value = line.split(":", 1)
                    self.metadata[key.strip()] = value.strip()
        

    def import_data(self):
        #extract and save the metadata
        self.extract_metadata()
        self.save_metadata()

        # Load data, skipping the first 5 rows containing metadata
        df = pd.read_csv(self.input_file, skiprows=5)
        
        # Define column mappings for column normalization
        column_mapping_xyz1 = {
                        'Temp [deg C]': 'Temperature [C]',
                        'Ah': 'Capacity [Ah]'
                    }
        df.rename(columns=column_mapping_xyz1, inplace=True)
        
        # Creation of new column that defines the testing duration
        # Ensure required column are present for this calculation
        if 'Time [s]' in df.columns:
            df['Testing_Time [s]'] = df['Time [s]'] - df['Time [s]'].iloc[0]
        else:
            raise ValueError("Required column 'Time [s]' is missing in the input file.")

        self.save_data_as_csv(df)
        




