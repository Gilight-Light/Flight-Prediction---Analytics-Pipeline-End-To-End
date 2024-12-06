import pandas as pd
import numpy as np
import os
import matplotlib as mp
import datetime

def Data_Transformation(read_economy, read_business):
    def convert_to_hours(time_str):
        hours, minutes = 0, 0
        if 'h' in time_str and time_str.split('h')[0].strip() != '':
            hours = float(time_str.split('h')[0].strip())
        if 'm' in time_str and time_str.split('h')[1].replace('m', '').strip() != '':
            minutes = float(time_str.split('h')[1].replace('m', '').strip())
        return hours + minutes / 60

    def categorize_time(time):
        hour = time.hour
        if 0 <= hour < 4:
            return 'Late_Night'
        elif 4 <= hour < 8:
            return 'Early_Morning'
        elif 8 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 16:
            return 'Afternoon'
        elif 16 <= hour < 20:
            return 'Evening'
        else:
            return 'Night'
        
    def get_stops(stop_value):
        if stop_value == 'non-stop':
            return 'zero'
        elif stop_value == '1-stop':
            return 'one'
        else:
            return 'two_or_more'



    ## Create list collumn ELT
    columns_to_keep = ['date', 'airline', 'flight', 'source_city', \
                    'departure_time', 'stops', 'arrival_time', 'destination_city', \
                    'class', 'duration', 'days_left', 'price']

    ## Data Transform
    df_combined = pd.concat([read_economy, read_business], axis=0, ignore_index=True)
    df_combined['stop'] = df_combined['stop'].str.replace(r'[\t"]', '', regex=True)
    df_combined['stop'] = df_combined['stop'].str.replace(r'[\n"]', '', regex=True)
    df_combined['stop'] = df_combined['stop'].str.replace(' ', '', regex=True)
    df_combined['hours'] = df_combined['time_taken'].apply(convert_to_hours)
    df_combined['days_left'] = (df_combined['hours'] // 24 + 1).astype(int)
    df_combined['duration'] = df_combined['hours'].round(2)
    df_combined['flight'] = df_combined['ch_code'] + '-'  + df_combined['num_code'].astype(str)
    df_combined.rename(columns={'from': 'source_city', 'to': 'destination_city'}, inplace=True)
    df_combined['arr_time'] = pd.to_datetime(df_combined['arr_time'], format='%H:%M')
    df_combined['arrival_time'] = df_combined['arr_time'].apply(categorize_time)
    df_combined['dep_time'] = pd.to_datetime(df_combined['dep_time'], format='%H:%M')
    df_combined['departure_time'] = df_combined['dep_time'].apply(categorize_time)
    df_combined['stops'] = df_combined['stop'].astype(str).apply(get_stops)
    df_selected = df_combined[columns_to_keep]
    df_selected['date'] = pd.to_datetime(df_selected['date'], format='%d-%m-%Y')

    ## Get Gold Data
    df_sorted = df_selected.sort_values(by='date',ascending=True)

    return df_sorted

## Save Gold Data into DataWareHouse