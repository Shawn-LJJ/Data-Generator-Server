import pandas as pd
import numpy as np
import random
import requests
import json
from functions.get_mockaroo import main as get_mockaroo_data
# from data_server.functions.get_mockaroo import main as get_mockaroo_data

# RESALE_DF = pd.read_csv('./data_server/data/random_local_address.csv')
RESALE_DF = pd.read_csv('./static/random_local_address.csv')

def unit_maker(row):
    lower_flr, _, upper_flr = row['storey_range'].split(' ')
    floor = str(int((int(lower_flr) + int(upper_flr)) / 2)).rjust(2, '0')
    rand_unit = str(random.randint(1, 999)).rjust(3, '0')
    return f'{floor}-{rand_unit}'

def postal_code(row):
    return f'{random.randint(100, 999)}{row["block"]}'

def add_a(row):
    if isinstance(row['address_id'], int):
        return f'A{row["address_id"]}'
    return pd.NA

def main(cust_df: pd.DataFrame, merc_df: pd.DataFrame, foreign_merc_perc: int, online_merc_perc: int) -> pd.DataFrame:

    # setting up how many address and local/foreign addresses needed
    cust_len = len(cust_df)
    merc_len = round(len(merc_df) * (100 - online_merc_perc) / 100)
    foreign_len = round(merc_len * foreign_merc_perc / 100)
    local_len = cust_len + (merc_len - foreign_len)

    # random sample the housing data
    rand_idx = np.random.choice(len(RESALE_DF), local_len, replace=False)
    random_local_df = RESALE_DF.iloc[rand_idx]

    # apply the functions
    random_local_df['unit_number'] = random_local_df.apply(unit_maker, axis=1)
    random_local_df['postal_code'] = random_local_df.apply(postal_code, axis=1)
    random_local_df.loc[:, 'country'] = 'Singapore'
    random_local_df.drop(columns=['storey_range'], inplace=True)

    # get the oversea address from mockaroo
    random_oversea_df = get_mockaroo_data('foreign_address', foreign_len)

    # combine the dataframe and append the data with address_id
    address_df = pd.concat([random_local_df, random_oversea_df], ignore_index=True)
    address_df['address_id'] = range(1, len(address_df) + 1)
    cust_df['address_id'] = range(1, cust_len + 1)
    merc_df['address_id'] = list(range(cust_len + 1, local_len + foreign_len + 1)) + [pd.NA] * (len(merc_df) - merc_len)

    # add letter a in front of every address_id
    address_df['address_id'] = address_df.apply(add_a, axis=1)
    cust_df['address_id'] = cust_df.apply(add_a, axis=1)
    merc_df['address_id'] = merc_df.apply(add_a, axis=1)

    return address_df