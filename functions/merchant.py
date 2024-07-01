import pandas as pd
import re

def extract_number(id_str):
    return int(re.search(r'\d+', id_str).group())

def main(df : pd.DataFrame) -> pd.DataFrame:

    # manually add banks
    current_max_id = max(df['merchant_id'].apply(extract_number))
    banks = [{'merchant_name' : bank, 'merchant_category' : 'Bank'} for bank in ['OCBC', 'POSB/DBS', 'CitiBank', 'UOB', 'Standard Chartered']]
    for i, row in enumerate(banks, start=1):
        new_id = f'M{current_max_id + i}'
        row['merchant_id'] = new_id
    bank_df = pd.DataFrame(banks)
    df = pd.concat([bank_df, df], ignore_index=True)

    return df