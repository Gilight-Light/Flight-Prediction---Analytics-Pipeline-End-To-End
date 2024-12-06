import os
import pandas as pd


def clean_data_extract():
    data_path_economy = '/tmp/economy.csv'
    data_path_business = '/tmp/business.csv'
    columns_to_keep = ['date', 'airline', 'ch_code', 'num_code', \
                   'dep_time', 'from', 'time_taken', 'stop', \
                   'arr_time', 'to', 'price', 'class']
    ## Load data into DataFrame
    data_economic = pd.read_csv(data_path_economy)
    data_business = pd.read_csv(data_path_business)
    
    data_economic['stop'] = data_economic['stop'].str.replace(r'[\t"]', '', regex=True)
    data_economic['stop'] = data_economic['stop'].str.replace(r'[\n"]', '', regex=True)
    data_economic['stop'] = data_economic['stop'].str.replace(' ', '', regex=True)
    data_economic["price"] = data_economic["price"].astype(str).str.replace(",", "").astype(int)
    data_economic['class'] = 'Economy'
    data_economic = data_economic[columns_to_keep]

    data_business['stop'] = data_business['stop'].str.replace(r'[\t"]', '', regex=True)
    data_business['stop'] = data_business['stop'].str.replace(r'[\n"]', '', regex=True)
    data_business['stop'] = data_business['stop'].str.replace(' ', '', regex=True)
    data_business["price"] = data_business["price"].astype(str).str.replace(",", "").astype(int)
    data_business['class'] = 'Business'
    data_business = data_business[columns_to_keep]

    data_economic.to_csv(data_path_economy, index=False, mode='w')
    data_business.to_csv(data_path_business, index=False, mode='w')



    
