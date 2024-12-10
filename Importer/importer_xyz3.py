import pandas as pd
from Importer.base_importer import BaseImporter


class ImporterXYZ3(BaseImporter) :
    def __init__(self, input_file, output_dir='results'):
        super().__init__(input_file, output_dir)
    
    def extract_metadata(self):
        metadata_started = False

        with open(self.input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("[Section 1]"):
                    break
                if line.startswith("[") and line.endswith("]"):
                    metadata_started = True
                elif metadata_started and line:
                    if ":;" in line:
                        key, value = line.split(":;", 1)
                        self.metadata[key.strip()] = value.strip()
                    else:
                        print(f"Skipping invalid line: {line}")
          

    def import_data(self):
        #extract and save the metadata
        self.extract_metadata()
        self.save_metadata()

        # Load data
        df = pd.read_csv(self.input_file, sep = ";", skiprows=41, dtype= {'Date':str, 'Time':str} )
        df = df[1:]
        
        # Define column mappings for column normalization
        column_mapping_xyz3 = {
            'Date': 'Date',
            'Time': 'Time',
            'Step': 'Step',
            'Profile_time': 'Profile_Time',
            'Step_time': 'Step_Time',
            'Loop_level': 'Loop_Level',
            'Loop_no': 'Loop_No',
            'Voltage': 'Voltage [V]',
            'Current': 'Current [A]',
            'Temperature': 'Temperature [C]',
            'Capacity': 'Capacity [Ah]',
            'AhStep': 'Capacity_per_Step [Ah/Step]',
            'Energy': 'Energy [Wh]',
            'WhStep': 'Energy_per_Step [Wh/Step]'
}
        df.rename(columns=column_mapping_xyz3, inplace=True)

        # Calculation of testing time from 'Date' and 'Time' column 
        df['Timestamp'] = df['Date'] + ' ' +  df['Time']
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Testing_Time [s]'] = (df['Timestamp'] - df['Timestamp'].iloc[0]).dt.total_seconds()

        # Keep only data points where we have measures
        df= df[df["Circuit_action"] != 'Message']

        self.save_data_as_csv(df)
        