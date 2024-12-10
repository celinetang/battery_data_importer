import os
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio

def find_csv_files_in_first_sublayer(directory):
    csv_files = []
    try:
        # Get first-level subdirectories
        subdirs = next(os.walk(directory))[1]  
        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            if os.path.isdir(subdir_path):
                for file in os.listdir(subdir_path):
                    if file.endswith(".csv"):
                        csv_files.append(os.path.join(subdir_path, file))
    except StopIteration:
        print(f"No subdirectories found in {directory}")
    return csv_files

# Specify the directory to search
directory_path = 'results'

csv_files = find_csv_files_in_first_sublayer(directory_path)

print("CSV files found:")
for file in csv_files:
    print(file)

# Combine and plot CSV files
combined_data = []

for file in csv_files:
    df = pd.read_csv(file)
    # Add a column to identify the source CSV file
    df['source'] = os.path.basename(file)  
    combined_data.append(df)

# Concatenate all dataframes
combined_df = pd.concat(combined_data, ignore_index=True)

# Plotting all data on the same figure
fig = go.Figure()

for file in csv_files:
    df = combined_df[combined_df['source'] == os.path.basename(file)]
    fig.add_trace(go.Scatter(x=df['Testing_Time [s]'], y=df['Voltage [V]'], mode='lines', name=os.path.basename(file)))

fig.update_layout(title='Combined CSV Data Plot', xaxis_title='Time [s]', yaxis_title='Voltage [V]')
fig.show()

# Save the figure as a PNG file in the results directory
output_path = os.path.join(directory_path, 'Voltage [V] over Time [s].png')
pio.write_image(fig, output_path)
print(f"Figure saved as {output_path}")
