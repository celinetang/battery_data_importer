import pandas as pd
import re
from Importer.base_importer import BaseImporter


class ImporterXYZ2(BaseImporter) :
    def __init__(self, input_file, output_dir='results'):
        super().__init__(input_file, output_dir)
    
    def extract_metadata(self):
        with open(self.input_file, 'r') as file:
                first_line = file.readline().strip()
                # Extracting segments of metadata
                todays_date_pattern = re.compile(r"Today's Date (\d{2}/\d{2}/\d{4})")
                date_of_test_pattern = re.compile(r"Date of Test:\s+(\d{2}/\d{2}/\d{4})")
                filename_pattern = re.compile(r"Filename:\s+([^\s]+)")
                procedure_pattern = re.compile(r"Procedure:\s+([^\t]+)")
                comment_barcode_pattern = re.compile(r"Comment/Barcode:\s+([^\t]+)")

                # Extracting the values using the patterns
                todays_date_match = todays_date_pattern.search(first_line)
                date_of_test_match = date_of_test_pattern.search(first_line)
                filename_match = filename_pattern.search(first_line)
                procedure_match = procedure_pattern.search(first_line)
                comment_barcode_match = comment_barcode_pattern.search(first_line)

                # Creating the metadata dictionary
                self.metadata = {
                        "Today's Date": todays_date_match.group(1) if todays_date_match else None,
                        "Date of Test": date_of_test_match.group(1) if date_of_test_match else None,
                        "Filename": filename_match.group(1).strip() if filename_match else None,
                        "Procedure": procedure_match.group(1).strip() if procedure_match else None,
                        "Comment/Barcode": comment_barcode_match.group(1).strip() if comment_barcode_match else None,
                    }

        
        

    def import_data(self):
        #extract and save the metadata
        self.extract_metadata()
        self.save_metadata()

        # Load data
        df = pd.read_csv(self.input_file, delimiter='\t', skiprows=1, index_col=False)
        
        # Define column mappings for column normalization
        column_mapping_xyz2 = {
                'Cyc#': 'Cycle',
                'Test (Sec)': 'Test_Time [s]',
                'Step (Sec)': 'Step_Time [s]',
                'Amp-hr': 'Capacity [Ah]',
                'Watt-hr': 'Energy [Wh]',
                'Amps': 'Current [A]',
                'Volts': 'Voltage [V]',
                'DPt Time': 'Data_Point_Time',
                'ACImp/Ohms': 'AC_Impedance [Ohm]',
                'DCIR/Ohms': 'DCIR [Ohm]',
                'Aux #1': 'Aux1',
                'Aux #2': 'Aux2',
                'Aux #3': 'Aux3',
                'Aux #4': 'Aux4'
            }
        df.rename(columns=column_mapping_xyz2, inplace=True)

        # Calculation of testing time can be from the Data_Point_Time column or the Test_time [s] column
        # Both have been tried and are equivalent
        if 'Data_Point_Time' not in df.columns:
            raise ValueError("Required column 'Data_Point_Time' is missing in the input file.")

        df['Timestamp'] = pd.to_datetime(df['Data_Point_Time'])
        df['Testing_Time [s]'] = (df['Timestamp'] - df['Timestamp'].iloc[0]).dt.total_seconds()
        
        self.save_data_as_csv(df)
        