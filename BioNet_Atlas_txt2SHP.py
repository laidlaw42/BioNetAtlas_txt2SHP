import geopandas as gpd
from shapely.geometry import Point
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def process_file():
    input_file = input_entry.get()
    if not input_file.endswith('.txt'):
        tk.messagebox.showerror('Invalid File', 'Please select a valid .txt file.')
        return

    selected_epsg = epsg_combobox.get()
    current_date = datetime.now().strftime('%Y%m%d')

    output_shapefile = f"{input_file[:-4]}_EPSG{selected_epsg}_{current_date}"
    output_txt_file = f"{input_file[:-4]}_EPSG{selected_epsg}_{current_date}.txt"
    output_csv_file = f"{input_file[:-4]}_EPSG{selected_epsg}_{current_date}.csv"

    try:
        features = remove_first_four_lines_and_convert(input_file, output_shapefile)

        save_to_txt(output_txt_file, features)
        save_to_csv(output_csv_file, features)

        tk.messagebox.showinfo('Success', f'The file has been processed and saved as {output_shapefile}, {output_txt_file}, and {output_csv_file}.')
    except Exception as e:
        print(f"Error during processing: {e}")
        tk.messagebox.showerror('Error', 'An error occurred during processing. Please check the console for details.')

# Modify this function as mentioned in the previous response
def remove_first_four_lines_and_convert(input_file, output_shapefile):
    with open(input_file, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    lines = lines[4:]
    headers = lines[0].strip().split('\t')

    if 'Easting' not in headers or 'Northing' not in headers:
        print('Header "Easting" or "Northing" not found.')
        return

    features = []

    try:
        for line in lines[1:]:
            values = line.strip().split('\t')
            x, y = map(float, (values[headers.index('Easting')], values[headers.index('Northing')]))

            feature = {'geometry': Point(x, y), 'Easting': x, 'Northing': y}

            for header, value in zip(headers, values):
                if header != 'Easting' and header != 'Northing':
                    feature[header] = value

            features.append(feature)

    except Exception as e:
        print(f"Error: {e}")

    gdf = gpd.GeoDataFrame(features, geometry='geometry', crs=f'EPSG:{epsg_combobox.get()}')
    gdf.to_file(output_shapefile)

    return features

def save_to_txt(output_txt_file, features):
    # Save processed data to a new text file
    with open(output_txt_file, 'w', encoding='utf-8') as txt_output:
        # Write headers
        header_line = '\t'.join(features[0].keys()) + '\n'
        txt_output.write(header_line)

        # Write data
        for feature in features:
            data_line = '\t'.join(str(value) for value in feature.values()) + '\n'
            txt_output.write(data_line)

def save_to_csv(output_csv_file, features):
    # Save processed data to a CSV file
    with open(output_csv_file, 'w', encoding='utf-8') as csv_output:
        # Write headers
        header_line = ','.join(features[0].keys()) + '\n'
        csv_output.write(header_line)

        # Write data
        for feature in features:
            data_line = ','.join(str(value) for value in feature.values()) + '\n'
            csv_output.write(data_line)

# Create the main application window
app = tk.Tk()
app.title('BioNet Atlas Text file to Shapefile Converter')

# Create and place widgets
input_label = tk.Label(app, text='Select the text file:')
input_label.grid(row=0, column=0, padx=10, pady=10)

input_entry = tk.Entry(app, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)

browse_button = tk.Button(app, text='Browse', command=select_input_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Create a Combobox for EPSG selection
epsg_label = tk.Label(app, text='Select EPSG:')
epsg_label.grid(row=1, column=0, padx=10, pady=10)

epsg_combobox = ttk.Combobox(app, values=['28355', '28356','7856','7855'])
epsg_combobox.grid(row=1, column=1, padx=10, pady=10)
epsg_combobox.set('28356')  # Set default selection

process_button = tk.Button(app, text='Run, fly, or swim', command=process_file)
process_button.grid(row=2, column=0, columnspan=3, pady=10)

# Start the application
app.mainloop()