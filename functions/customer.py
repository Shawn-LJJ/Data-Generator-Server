import pandas as pd
import random
from scipy.stats import skewnorm
import math

def ic_maker(row):
    birth_year = 2024 - row['age']
    birth_seq = f'{random.randint(1, 99999)}'.rjust(5, '0')
    first_char = 'S' if birth_year < 2000 else 'T'
    return first_char + str(birth_year)[2:] + birth_seq + random.choice('QWERTYUIOPASDFGHJKLZXCVBNM')

def address_maker(row, num_of_rows):
    add_id = int(row['customer_id'][1:])
    cut_off = round(num_of_rows * 9 / 10)
    add_id = add_id % cut_off
    return 'A' + str(cut_off if add_id == 0 else add_id)

def income_maker(row):
    age = row['age']
    if 0.98 * math.sin(1.26 * math.log(18 * age - 150)) < random.random():
        return 0
    mean_income = (-1.5 * age ** 2) + (160 * age) - 800
    std_dev = 800 * math.log(age - 16)
    skewness = round((-1/500) * age ** 2 + 0.25 * age)
    return int(round(skewnorm.rvs(skewness, loc=mean_income, scale=std_dev, size=1)[0], -2))

def add_credit_limit_flag_up(row):
    
    yearly_income = row['income'] * 12
    monthly_income = row['income']

    if yearly_income <= 15000:
        if row['age'] <= 55:
            return 0, 0
        return 2500, 1250
    elif yearly_income <= 30000:
        return monthly_income * 2, monthly_income
    elif yearly_income <= 120000:
        return monthly_income * 4, monthly_income * 2
    else:
        return pd.NA, pd.NA

add_flag_up_value = lambda row : row['credit_limit'] / 2

def main(df:pd.DataFrame) -> pd.DataFrame:
    df['NRIC'] = df.apply(ic_maker, axis=1)
    df['address_id'] = df.apply(lambda row: address_maker(row, len(df)), axis=1)
    df['income'] = df.apply(income_maker, axis=1)
    df[['credit_limit', 'flag_up_value']] = df.apply(add_credit_limit_flag_up, axis=1, result_type='expand')
    return df