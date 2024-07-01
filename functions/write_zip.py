import pandas as pd
import zipfile
from io import BytesIO
from time import time_ns

def main(cust_df: pd.DataFrame, merc_df: pd.DataFrame, address_df: pd.DataFrame, cc_df: pd.DataFrame) -> str:

    timestamp = str(time_ns())[2:-3]
    zip_file_path = f'./zip/{timestamp}.zip'
    df_dict = {
        'customer.csv' : cust_df,
        'merchant.csv' : merc_df,
        'address.csv' : address_df,
        'credit_card.csv' : cc_df
    }

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name, df in df_dict.items():
            # write df to CSV in memory
            with BytesIO() as buffer:
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                zipf.writestr(file_name, buffer.read())
    
    return zip_file_path