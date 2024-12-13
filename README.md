# Take Home Exercise
At V***, a big portion of our job is being able to create and develop importers for various types of customer data. In this exercise, you will be tasked with creating a basic importer that allows you to import data files in various formats.

1. Each file import should be able to be triggered with a single function call.
2. For as many of the test files complete the following.
   * Extract the metadata at the top of the data file. Write the metadata as key value pairs in a txt file to the results directory.
   * Import the data and write it as a csv in the results directory. Feel free to use any python packages to accomplish this task.
3. Plot all voltage traces across all files as a function of time in a single figure. Use any python-based plotter such as matplotlib, plotly, bokeh, etc.
4. Save the figure as a `.png` to the results folder.

**It is okay if you do not manage to get all the datafiles imported**, the focus of this exercise is the design of the importer. It may help to think about the importer in the context of configurability.

Some configuration options we recommend:
   * File path to read in
   * File path to output to
   * Normalization of units and column names

Use the differences in the data files to inspire more configuration options.

**Please do not spend more than four hours on this project.**

If you get stuck or have any questions, don't hesitate to reach out!

# Evaluation Guidelines
* Code clarity/readability
* Testing
* Requirements fulfilled
* Documentation

------------------------------------------------------------------------------------------------------------

# Data Importer Project

The Data Importer project is designed to import data from various file formats (e.g., .xyz, .mdb) and process them according to specific importers. 

The project supports different formats by identifying the type of file and applying the corresponding importer logic. The results are saved in a structured output directory called results.

# Structure

Inside the Importer folder : 
    1. base_importer.py: Defines the BaseImporter class, which provides common functionality for all importers.
    2. importer_xyz1.py: Defines the ImporterXYZ1 class for a specific type of .xyz file.
    3. importer_xyz2.py: Defines the ImporterXYZ2 class for another type of .xyz file.
    4. importer_xyz3.py: Defines the ImporterXYZ3 class for a third type of .xyz file.
    5. importer_mdp.py : Defines the ImporterMDB class for .mdb file.
    6. data_importer.py: Contains the DataImporter class, which chooses which importer to use according to the input file.

In the main folder : 
    - main.py: Entry point for the application
            - Each file import is triggered with a single function call : import_file()
            - For as many of the test files :
                * Extract the metadata at the top of the data file. Write the metadata as key value pairs in a txt file to the results directory.
                * Import the data and write it as a csv in the results directory.
    - plot_traces.py : 
            - Plot all voltage traces across all files as a function of time in a single figure using Plotly.
            - Save the figure as a `.png` to the results folder.
    - requirements.txt : required packages to install for the code to work properly.


# How It Works

    Initialization:
        The DataImporter class is initialized with the path to the input file.

    Importer Selection:
        The DataImporter class determines the appropriate importer class based on the file extension and, in the case of .xyz files, the contents of the file.
        The get_importer method retrieves the correct importer class.
        For .xyz files, the get_xyz_importer method reads the first line of the file to decide between ImporterXYZ1, ImporterXYZ2, and ImporterXYZ3.

    Data Import:
        The import_file method in DataImporter instantiates the appropriate importer class with the input file and output file paths.
        The importer class processes the file and saves the results.

    Output Structure:
        The results are saved in a result directory.
        Inside the result directory, a subdirectory named after the input file is created.
        Metadata is saved as <basename>_metadata.txt.
        Data is saved as <basename>.csv.

# Usage

1. Ensure all necessary files are available and install the required packages listed in requirements.txt.
    Create a virtual environment in order to install all requirements

    python3 -m venv importer-venv
    source importer-venv/bin/activate
    pip install -r requirements.txt

2. Run the application for all files in test_files :

    python main.py 

You should obtain a results folder with as many subfolders as test_files


3. Plot all voltage traces across all files as a function of time :

    python plot_traces.py

You should obtain a .png figure in the results folder
The dynamic version of the graph opens up automatically. The various graphs we obtain should be compared, but in this specific examples the voltages are not valid. 

# To go further :

- In this example, it was only required to plot voltage as a function of time. It would be interesting to create a new class to plot traces of other variables over time, and choose according to which data is available in each test_files

- Due to shortage of time, code was not optimally refactored. It is possible to refactor the main.py and plot_traces.py

- Work more on the Error Handling and Warnings : including the ParseWarnings obtained

- Further study which metadata that we want to keep for the .mdb importer

- Instead of making the user rebuild the environmment, directly create a Dockerfile so you can have a ready-made environment to run the code 

- Note : the 4 files don't show any interesting battery data to compare. The batteries are either at OCV and will start cycling soon. 
