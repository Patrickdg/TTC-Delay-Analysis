# TTC-Delay-Analysis
Exploratory Analysis of the Toronto Transit Commission (TTC) Delay data from the City of Toronto data portal, cross-examined with historical TTC ridership statistics and Toronto weather data.

# Synopsis


# Data Sources

## Transportation Mode Delay Data
TTC delay data was sourced for the following modes: [Subway](https://open.toronto.ca/dataset/ttc-subway-delay-data/), [Streetcar](https://open.toronto.ca/dataset/ttc-streetcar-delay-data/), [Bus](https://open.toronto.ca/dataset/ttc-bus-delay-data/)

## TTC Ridership Data
The TTC ridership data was sourced from the [City of Toronto website, Progress Portal](https://www.toronto.ca/city-government/data-research-maps/toronto-progress-portal/).

From the above site, using the 'Export Data' option, the 2 measures included in the data extract were:
- 'TTC Average Weekday Ridership', and
- 'TTC Monthly Ridership
Selecting these measures will output the raw .csv file found in the './data/raw/ridership/TorontoMeasureData.csv'
path within this repository.

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
## Subway Delay Data
Subway data was processed into a single .csv file within the 'data/processed' folder after processing within the '1 - Data Gathering and Cleaning.py' script.

Within the total subway dataset (~112,000 observations), approximately 24,000 observations were missing values in the 'bound' column (i.e., direction of the route when the incident took place).
From closer review, most of these observations were of the following incidents:
- MUGD: Miscellaneous General Delays (4950 observations)
- MUIS: Injured or ill Customer (In Station) - Transported (4771 observations)
- MUO: Miscellaneous Other (3297 observations)
- PUMEL: Escalator/Elevator Incident (2386 observations)
- MUNCA: No Operator Immediately Available - Not E.S.A. Related (2148 observations)
- MUIRS: Injured or ill Customer (In Station) - Medical Aid Refused (918 observations)

The majority of these incidents occurred within station or outside of vehicle. Therefore, missing values for 'bound' is expected for these incident types.

Similar analysis was performed on the ~500 observations with missing 'line' values. These observations were of 'Miscellaneous General Delays' and 'Miscellaneous Other' incident types.

Therefore, missing values within the subway data set was kept within the final processed set.

Missing values within the 'vehicle' column (for incidents not occurring within any particular subway vehicle) were denoted originally as '0' and replaced with NaN.

## Streetcar Delay Data
For simplicity, minor cleaning was performed manually on streetcar files to address the following:
- Inconsistent column 'Incident ID' deleted from 'ttc-streetcar-delay-data-2019.xlsx', 'Apr 2019' worksheet
- Inconsistent column names 'Delay' and 'Gap' changed to 'Min Delay' and 'Min Gap' from 'ttc-streetcar-delay-data-2019.xlsx', 'Apr 2019' and 'June 2019' worksheets
- Inconsistent 'Time' values found at '2017-05-27 00:00:00' and '2016-03-10 00:00:00' coerced to 00:00:00

Similar to the above processing performed on the subway dataset, missing values within the 'vehicle' column were denoted originally with '0' and replaced with NaN.


## Bus Delay Data
## TTC Ridership Data

## Weather Data


