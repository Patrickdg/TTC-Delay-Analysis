# TTC-Delay-Analysis
Exploratory Analysis of the Toronto Transit Commission (TTC) Delay data from the City of Toronto data portal, cross-examined with historical TTC ridership statistics and Toronto weather data.

# Synopsis


# Data Sources


## TTC Ridership Data
The TTC ridership data was sourced from the [City of Toronto website, Progress Portal](https://www.toronto.ca/city-government/data-research-maps/toronto-progress-portal/).

From the above site, using the 'Export Data' option, the 2 measures included in the data extract were:
- 'TTC Average Weekday Ridership', and
- 'TTC Monthly Ridership
Selecting these measures will output the raw .csv file found in the './data/TorontoMeasureData.csv'
path within this repository.

## Transportation Mode Delay Data
TTC delay data was sourced for the following modes: [Subway](https://open.toronto.ca/dataset/ttc-subway-delay-data/), [Streetcar](https://open.toronto.ca/dataset/ttc-streetcar-delay-data/), [Bus](https://open.toronto.ca/dataset/ttc-bus-delay-data/)

## Canada Weather Data
Weather data was sourced from the [Canada Weather Stats website](https://www.weatherstats.ca/).

Hourly data was extracted to allow for extra granularity when analyzing relationships between weather and TTC delays.
Daily data was extracted to capture snow and rain data per day (as hourly data set did not contain these features).

This data was extracted manually from the data download page of the Canada Weather Stats website (found [here](https://toronto.weatherstats.ca/download.html)) with the following parameters selected:
**Daily Climate Data parameters:**
- 'Climate Daily/Forecast/Sun'
- Row limit: 2200

**Hourly Climate Data parameters:**
- 'Climate Hourly'
- Row limit: 50000

# Data Cleaning & Processing

## TTC Ridership Data
## Subway Delay Data
- Column names are changed to lower case
- 'datetime' column created by concatenating 'date' and 'time' columns from original data
-

## Streetcar Delay Data
## Bus Delay Data

## Weather Data


