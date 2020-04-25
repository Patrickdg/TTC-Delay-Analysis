# TTC-Delay-Analysis
Exploratory Analysis of the Toronto Transit Commission (TTC) Delay data from the City of Toronto data portal, cross-examined with historical TTC ridership statistics and Toronto weather data.

# Data Sources

## Transportation Mode Delay Data
TTC delay data was sourced for the following modes: [Subway](https://open.toronto.ca/dataset/ttc-subway-delay-data/), [Streetcar](https://open.toronto.ca/dataset/ttc-streetcar-delay-data/), [Bus](https://open.toronto.ca/dataset/ttc-bus-delay-data/)

[See data gathering script](https://github.com/Patrickdg/TTC-Delay-Analysis/blob/master/data_gathering.py)

## TTC Ridership Data
The TTC ridership data was sourced from the [City of Toronto website, Progress Portal](https://www.toronto.ca/city-government/data-research-maps/toronto-progress-portal/).

From the above site, using the 'Export Data' option, the 2 measures included in the data extract were:
- 'TTC Average Weekday Ridership', and
- 'TTC Monthly Ridership
Selecting these measures will output the raw .csv file 'TorontoMeasureData.csv' within this repository.

## Canada Weather Data
Weather data was sourced from the [Canada Weather Stats website](https://www.weatherstats.ca/).

Hourly data was extracted to allow for extra granularity when analyzing relationships between weather and TTC delays.
Daily data was extracted to capture snow and rain data per day (as hourly data set did not contain these features).

This data was extracted manually from the data download page (found [here](https://toronto.weatherstats.ca/download.html)) with the following parameters selected:

**Daily Climate Data parameters:**
- 'Climate Daily/Forecast/Sun'
- Row limit: 2200

**Hourly Climate Data parameters:**
- 'Climate Hourly'
- Row limit: 50000


# Data Cleaning & Processing

## Subway, Streetcar, and Bus Delay Data

## TTC Ridership Data

## Weather Data


