import pandas as pd 
import numpy as np
import os
from collections import Counter

# TTC DATA
subway_path = 'data/raw/ttc/subway/'
streetcar_path = 'data/raw/ttc/streetcar/'
bus_path = 'data/raw/ttc/bus/'

## SUBWAY
def collapse_cols(col_list):
    return ' '.join([str(c) for c in col_list])

def build_column_names(path):
    column_names = []
    for xl in os.listdir(path):
        cols = pd.read_excel(f'{path}{xl}').columns
        cols = collapse_cols(cols)
    column_names.append(cols)

    return column_names

def check_inconsistent_cols(path, columns):
    for xl in os.listdir(path):
        cols = pd.read_excel(f'{path}{xl}').columns
        cols = collapse_cols(cols)

        if cols != columns: 
            print(f"Inconsistent columns: {xl}")

column_names = build_column_names(subway_path)
subway_columns, count = Counter(column_names).most_common()[0]

check_inconsistent_cols(subway_path, subway_columns)
 
### Move readmes and delay codes
to_be_moved = ['data/raw/ttc/subway/ttc-subway-delay-codes.xlsx', 
                'data/raw/ttc/subway/ttc-subway-delay-readme.xlsx',
                'data/raw/ttc/streetcar/ttc-streetcar-delay-data-readme.xlsx',
                'data/raw/ttc/bus/ttc-bus-delay-data-readme.xlsx']

try: 
    os.mkdir(r'data/raw/ttc/docs/')
except: 
    pass

for xl in to_be_moved:
    file_name = xl[xl.rfind(r'/')+1:]
    try: 
        os.rename(xl, f"data/raw/ttc/docs/{file_name}")
    except FileNotFoundError:
        print(f"{file_name} moved.")

### Compile into single file
columns = subway_columns.split()
subway_data = pd.DataFrame()

subway_file_path = 'data/processed/ttc/subway/subway_data.csv'
if not os.path.exists(subway_file_path):
    for xl in os.listdir(subway_path):
        df = pd.read_excel(f'{subway_path}{xl}')
        subway_data = pd.concat([subway_data, df])
    subway_data.to_csv(subway_file_path)


## STREETCAR
def compile_sheets(raw_path, dest_path):
    data = []
    if not os.path.exists(dest_path):
        for xl in os.listdir(raw_path):
            df = pd.read_excel(f"{raw_path}{xl}", sheet_name=None)
            df = pd.concat(df, ignore_index=True)
            data.append(df)
    data = pd.concat(data)

    return data

streetcar_file_path = 'data/processed/ttc/streetcar/streetcar_data.csv'
if not os.path.exists(streetcar_file_path):
    streetcar_data = compile_sheets(streetcar_path, streetcar_file_path)

    ### Fix inconsistent columns & Reorder
    streetcar_data['Min Delay'].fillna(streetcar_data['Delay'], inplace = True)
    del streetcar_data['Delay']
    streetcar_data['Min Gap'].fillna(streetcar_data['Gap'], inplace = True)
    del streetcar_data['Gap']
    del streetcar_data['Incident ID']

    streetcar_data = streetcar_data[['Report Date', 'Route', 'Time', 'Day', 
                                    'Location', 'Incident', 'Min Delay', 
                                    'Min Gap', 'Direction', 'Vehicle']]

    streetcar_data.to_csv(streetcar_file_path)


## BUS
bus_file_path = 'data/processed/ttc/bus/bus_data.csv'
if not os.path.exists(bus_file_path):
    bus_data = compile_sheets(bus_path, bus_file_path)

    ## Fix inconsistent columns & Reorder
    bus_data['Min Delay'].fillna(bus_data[' Min Delay'], inplace = True)
    del bus_data[' Min Delay']
    bus_data['Min Delay'].fillna(bus_data['Delay'], inplace = True)
    del bus_data['Delay']
    bus_data['Min Gap'].fillna(bus_data['Gap'], inplace = True)
    del bus_data['Gap']
    del bus_data['Incident ID']

    bus_data = bus_data[['Report Date', 'Route', 'Time', 'Day', 
                                    'Location', 'Incident', 'Min Delay', 
                                    'Min Gap', 'Direction', 'Vehicle']]

    bus_data.to_csv(bus_file_path)