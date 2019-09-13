# Required Libraries
import os
import urllib.request
import pandas as pd
import numpy as np
import json

#==============================================================================#
# INITIAL DIRECTORY SETUP
if not os.path.exists('data/'):
   directories = ['data/',
                  'data/raw','data/raw/ridership',
                  'data/raw/ttc','data/raw/ttc/subway','data/raw/ttc/subwaycodes',
                  'data/raw/ttc/streetcar','data/raw/ttc/bus','data/raw/weather',
                  'data/processed']

   for directory in directories:
      os.mkdir(directory)

#==============================================================================#
# DATA GATHERING

## TTC SUBWAY DELAY DATA (AND ACCOMPANYING CODE BOOK)
if len(os.listdir('data/raw/ttc/subway')) == 0:
   url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
   params = { "id": "996cfe8d-fb35-40ce-b569-698d51fc683b"}
   response = urllib.request.urlopen(url,
                                     data=bytes(json.dumps(params),
                                                encoding="utf-8"))
   package = json.loads(response.read())

   urls = pd.DataFrame(columns = ['item','url'])
   for i, file in enumerate(package['result']['resources']):
      urls.loc[i,'item'] = file['name']
      urls.loc[i,'url'] = file['url']

   for item, url in zip(urls.item, urls.url):
      urllib.request.urlretrieve(url = url,
                                 filename = 'data/raw/ttc/subway/{}.xlsx'.format(item))

   os.rename('data/raw/ttc/subway/ttc-subway-delay-codes.xlsx',
             'data/raw/ttc/subwaycodes/ttc-subway-delay-codes.xlsx')
   os.remove('data/raw/ttc/subway/ttc-subway-delay-readme.xlsx')

else:
   print("Check data/raw/ttc/subway directory. Files already exist.")

## TTC STREETCAR DELAY DATA
if len(os.listdir('data/raw/ttc/streetcar')) == 0:
   url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
   params = { "id": "b68cb71b-44a7-4394-97e2-5d2f41462a5d"}
   response = urllib.request.urlopen(url,
                                     data=bytes(json.dumps(params),
                                                encoding="utf-8"))
   package = json.loads(response.read())

   urls = pd.DataFrame(columns = ['item','url'])
   for i, file in enumerate(package['result']['resources']):
      urls.loc[i,'item'] = file['name']
      urls.loc[i,'url'] = file['url']

   for item, url in zip(urls.item, urls.url):
      urllib.request.urlretrieve(url = url,
                                 filename = 'data/raw/ttc/streetcar/{}.xlsx'.format(item))

   os.remove('data/raw/ttc/streetcar/ttc-streetcar-delay-data-readme.xlsx')

else:
   print("Check data/raw/ttc/streetcar directory. Files already exist.")

## TTC BUS DELAY DATA
if len(os.listdir('data/raw/ttc/bus')) == 0:
   url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
   params = { "id": "e271cdae-8788-4980-96ce-6a5c95bc6618"}
   response = urllib.request.urlopen(url,
                                     data=bytes(json.dumps(params),
                                                encoding="utf-8"))
   package = json.loads(response.read())

   urls = pd.DataFrame(columns = ['item','url'])
   for i, file in enumerate(package['result']['resources']):
      urls.loc[i,'item'] = file['name']
      urls.loc[i,'url'] = file['url']

   for item, url in zip(urls.item, urls.url):
      urllib.request.urlretrieve(url = url,
                                 filename = 'data/raw/ttc/bus/{}.xlsx'.format(item))

   os.remove('data/raw/ttc/bus/ttc-bus-delay-data-readme.xlsx')

else:
   print("Check data/raw/ttc/bus directory. Files already exist.")


#==============================================================================#
# PREPROCESSING FOR SQL IMPORT
## SUBWAY DATA
if not os.path.exists('data/processed/subway.csv'):

   sub_df = pd.DataFrame()
   for file in os.listdir('data/raw/ttc/subway'):
      df = pd.read_excel('data/raw/ttc/subway/{}'.format(file))
      sub_df = sub_df.append(df)

   col_names = pd.read_excel('data/raw/ttc/subway/ttc-subway-delay-december-2017.xlsx').columns
   sub_df.columns = col_names.str.lower()

   ### Processing: create 'datetime' column, delete unneeded rows, rearrange columns
   sub_df['datetime'] = pd.to_datetime(sub_df.date.astype('str')+ " " + sub_df.time.astype('str'))
   sub_df.drop(columns = ['time','date'], inplace = True)
   sub_df = sub_df.loc[:,['datetime','station','code','min delay',
                          'min gap','bound','line','vehicle']]

   sub_df.vehicle.replace(0, np.nan, inplace = True)
   sub_df.sort_values(by = 'datetime', inplace = True)
   sub_df.reset_index(drop = True, inplace = True)

   sub_df.bound = sub_df.bound.str.strip().str.lower().str.replace(r'/', "").str.replace('\\',"").str.replace('.',"").str.replace(r'?', "").str.replace("(","").str.replace(")","").str.replace("-","")
   sub_df.station= sub_df.station.str.strip().str.lower().str.replace(r'/', "").str.replace('\\',"").str.replace('.',"").str.replace(r'?', "").str.replace("(","").str.replace(")","").str.replace("-","").str.replace("station","").str.strip()
   sub_df.line = sub_df.line.str.strip().str.lower().str.replace(r'/', "").str.replace('\\',"").str.replace('.',"").str.replace(r'?', "").str.replace("(","").str.replace(")","").str.replace("-","").str.replace("  ","")

   sub_df.to_csv(r'data/processed/subway.csv', header = True, sep = ",")

else:
   print("Processed subway file already exists.")

## STREETCAR DATA
if not os.path.exists('data/processed/streetcar.csv'):

   sc = pd.DataFrame()
   for file in os.listdir('data/raw/ttc/streetcar'):
      book = pd.read_excel('data/raw/ttc/streetcar/{}'.format(file),
                           sheet_name = None)
      sc = sc.append(pd.concat(book))

   sc.reset_index(drop = True, inplace = True)

   sc.iloc[31699,2] = sc.iloc[31699,2].time()
   sc.iloc[47724,2] = sc.iloc[47724,2].time()

   sc['datetime'] = sc['Report Date'].astype('str') + " " + sc.Time.astype('str')
   sc['datetime'] = pd.to_datetime(sc.datetime, format = "%Y-%m-%d %H:%M:%S")

   sc.drop(columns = ['Report Date','Time'], inplace = True)
   sc = sc[['datetime','Location','Incident','Min Delay',
            'Min Gap','Direction','Route','Vehicle']]
   sc.columns = ['datetime','station','code','min delay','min gap','bound','line','vehicle']

   sc.vehicle.replace(0,np.nan, inplace = True)

   bound_map = {
         'nb': 'n',
         'sb':'s',
         'eb':'e',
         'wb':'w',
         'bw':'both',
         'b':'both',
         'up':'n',
         'down':'s',
         "bw's":'both',
         'dn':'s',
         'bws':'both',
         'bothways':'both',
         'west':'w',
         'east':'e',
         'north':'n',
         'south':'s',
         'both ways':'both',
         'both way': 'both'}

   sc.bound = sc.bound.str.lower().str.replace(r'/', "").str.replace('\\',"").str.replace('.',"").str.replace(r'?', "")
   sc.bound = sc.bound.map(bound_map)

   sc.station = sc.station.str.strip().str.lower().str.replace(r'/', "").str.replace('\\',"").str.replace('.',"").str.replace(r'?', "").str.replace("(","").str.replace(")","").str.replace("-","").str.replace("  ","").str.replace("'","")
   sc.line = sc.line.astype('str').str.strip().str.lower().str.replace(r'/', "").str.replace('\\',"").str.replace('.',"").str.replace(r'?', "").str.replace("(","").str.replace(")","").str.replace("-","").str.replace("  ","")

   sc.to_csv('data/processed/streetcar.csv')

else:
   print("Processed streetcar file already exists.")

## BUS DATA
if not os.path.exists('data/processed/bus.csv'):

   bus = pd.DataFrame()
   for file in os.listdir('data/raw/ttc/bus'):
      book = pd.read_excel('data/raw/ttc/bus/{}'.format(file),
                           sheet_name = None)
      bus = bus.append(pd.concat(book))

   bus.reset_index(drop = True, inplace = True)

   bus.iloc[[117196, 155934, 165427, 207350, 229711, 232357, 247934, 263908,
             267962, 275230, 286661, 297859, 336624, 337380, 337709, 341519,
             342344, 369498, 371172, 371712, 380770, 388571, 409915, 409916,
             412061, 416015, 423381], 2] = bus.iloc[[117196, 155934, 165427, 207350, 229711, 232357, 247934, 263908,
             267962, 275230, 286661, 297859, 336624, 337380, 337709, 341519,
             342344, 369498, 371172, 371712, 380770, 388571, 409915, 409916,
             412061, 416015, 423381], 2].apply(lambda x: x.time())

   bus['datetime'] = bus['Report Date'].astype('str') + " " + bus.Time.astype('str')
   bus['datetime'] = pd.to_datetime(bus.datetime, format = "%Y-%m-%d %H:%M:%S")

   bus.drop(columns = ['Report Date','Time'], inplace = True)
   bus = bus[['datetime','Location','Incident','Min Delay',
            'Min Gap','Direction','Route','Vehicle']]
   bus.columns = ['datetime','station','code','min delay',
                  'min gap','bound','line','vehicle']

   bus.bound = bus.bound.str.lower().str.replace(r'/', "").str.replace('\\',"").str.replace('.',"").str.replace(r'?', "")

   bound_map = {
         'nb': 'n',
         'sb':'s',
         'eb':'e',
         'wb':'w',
         'bw':'both',
         'b':'both',
         'up':'n',
         'down':'s',
         "bw's":'both',
         'dn':'s',
         'bws':'both',
         'bothways':'both',
         'west':'w',
         'east':'e',
         'north':'n',
         'south':'s',
         'both ways':'both',
         'both way': 'both'}

   bus.bound = bus.bound.map(bound_map)

   bus.station = bus.station.str.strip().str.lower().str.replace('/',"").str.replace(r'\\',"").str.replace('.',"").str.replace(",","").str.replace("&","and")

   bus.to_csv('data/processed/bus.csv', header = True, sep = ",")

else:
   print("Processed bus file already exists.")

## RIDERSHIP DATA
if not os.path.exists('data/processed/ridership.csv'):
   r = pd.read_csv('data/raw/ridership/TorontoMeasureData.csv')
   r = pd.pivot_table(r, index = ['Year','Period'], columns = 'Measure Name', values = 'Value')
   r.to_csv('data/processed/ridership.csv', header = True, sep = ',', )
else:
   print("Processed ridership fil exists.")

## WEATHER DATA
if not os.path.exists('data/processed/weather.csv'):
   w_h = pd.read_csv('data/raw/weather/weatherstats_toronto_hourly.csv')
   w_h['date_time_local'] = pd.to_datetime(w_h['date_time_local'])

   w = pd.read_csv('data/raw/weather/weatherstats_toronto_daily.csv')[['date','precipitation','rain','snow','snow_on_ground']]
   w.date = pd.to_datetime(w.date)
   w.set_index('date', inplace = True)

   ### Processing
   w_h.drop(columns = ['unixtime','pressure_station','pressure_sea','wind_dir',
                       'wind_dir_10s','dew_point','cloud_cover_4','cloud_cover_8',
                       'cloud_cover_10','solar_radiation','humidex'],
            inplace = True)
   w_h[['wind_speed','wind_gust','windchill']] = w_h[['wind_speed','wind_gust','windchill']].replace(np.nan, 0)

   w.replace(np.nan, 0, inplace = True)

   w_h = pd.merge(w_h, w, how = 'left', left_on = w_h['date_time_local'].dt.date ,right_on = w.index.date)
   w_h.drop(columns = ['key_0'], inplace = True)
   w_h.replace('nan',np.nan, inplace = True)
   w_h.dropna(axis = 0, inplace = True)
   w_h.set_index('date_time_local', inplace = True)

   w_h.to_csv('data/processed/weather.csv', header = True, sep = ',')
else:
   print("Processed weather file already exists.")








