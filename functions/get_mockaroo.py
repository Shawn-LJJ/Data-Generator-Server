import requests
from io import StringIO
import pandas as pd

def main(field: str, rows: int) -> pd.DataFrame:
    url = f'https://my.api.mockaroo.com/{field}.json?key=9489d780&rows={rows}'
    response = requests.request("GET", url)
    csv_data = StringIO(response.text)
    return pd.read_csv(csv_data)