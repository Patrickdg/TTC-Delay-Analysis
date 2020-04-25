import pandas as pd 
import numpy as np
import os
from collections import Counter

# TTC DATA
## SUBWAY
subway_path = 'data/raw/ttc/subway/'

def collapse_cols(col_list):
    return ' '.join([str(c) for c in col_list])

def build_column_names(path):
    column_names = []
    for xl in os.listdir(subway_path):
        cols = pd.read_excel(f'{subway_path}{xl}').columns
        cols = collapse_cols(cols)

    column_names.append(cols)
    return column_names

def check_inconsistent_cols(path, columns):
    for xl in os.listdir(path):
        cols = pd.read_excel(f'{subway_path}{xl}').columns
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

n = 0
for xl in os.listdir(subway_path):
    df = pd.read_excel(f'{subway_path}{xl}')
    subway_data = pd.concat([subway_data, df])

subway_file_path = 'data/processed/ttc/subway/subway_data.csv'
if not os.path.exists(subway_file_path):
    subway_data.to_csv(subway_file_path)


## STREETCAR
