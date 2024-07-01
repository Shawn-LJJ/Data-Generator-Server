import pandas as pd
import random
import numpy as np

def make_link_cust(row, num_cust):
    id = int(row['credit_card_id'][2:])
    if id > num_cust:
        return f'C{id % num_cust}'
    return f'C{id}'

def main(df: pd.DataFrame, num_cust: int, bank_list) -> pd.DataFrame:
    df['customer_id'] = df.apply(lambda row: make_link_cust(row, num_cust), axis=1)
    df['merchant_id'] = random.choices(bank_list, k=len(df))
    return df