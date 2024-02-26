## BioNet Atlas Text file to Shapefile Converter

This script provides a GUI for converting the RAW data output (.txt) from [**BioNet Atlas**](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity/nsw-bionet)
 species sightings records into an ESRI Shapefile format.

It also cleans and creates a new text file, and renames all files adding CRS and date e.g.: 
*Atlas_records_abcdefg_EPSG7856_20240226.txt*

1. **GUI Setup**:
   - The script utilizes the `tkinter` library to create a GUI window titled "BioNet Atlas Text file to Shapefile Converter".
   - It includes widgets such as labels, entry fields, buttons, and a Combobox for EPSG selection.


2. **File Selection**:
   - Users can select a text file using the "Browse" button. Only `.txt` files are accepted.
   - The selected file path is displayed in an entry field.


3. **EPSG Selection**:
   - Users can choose an EPSG code from a Combobox. Default selection is EPSG code `28356`.


4. **Processing**:
   - Upon clicking the "Run, fly, or swim" button, the script processes the selected text file.
   - It checks if the file ends with `.txt`. If not, it displays an error message.
   - If the file is valid, it removes the first four lines and extracts data to convert to a shapefile.
   - The extracted data is then saved to a shapefile, TXT file, and CSV file using the selected EPSG code and the current date appended to the file names.


5. **Error Handling**:
   - Any errors that occur during processing are caught and displayed in both the console and a message box.


6. **Functions**:
   - `select_input_file()`: Opens a file dialog for selecting a text file.
   - `process_file()`: Initiates the file processing sequence.
   - `remove_first_four_lines_and_convert()`: Removes the first four lines of the input file, extracts relevant data, and saves it to a shapefile.
   - `save_to_txt()`: Saves processed data to a TXT file.
   - `save_to_csv()`: Saves processed data to a CSV file.

7. **Dependencies**:
   - The script relies on the `geopandas`, `shapely.geometry`, and `tkinter` libraries for spatial data processing and GUI creation.


8. **Execution**:
   - The script starts the application by running the main event loop (`app.mainloop()`), allowing users to interact with the GUI.
