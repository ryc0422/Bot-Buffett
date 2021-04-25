import requests
import time

from constants import BASE_URL


def get_stock_price(stock_code, timestamp=None):
    if timestamp is None:
        timestamp = int(time.time()*1000)
    stock_url = BASE_URL(stock_code=stock_code, timestamp=timestamp)
    print(stock_url)
    resp = requests.get(stock_url)
    raw_data = resp.json()

    if not raw_data['msgArray']: #not [] -> true
        return None

    price = raw_data['msgArray'][0]['z']
    name = raw_data['msgArray'][0]['n']
    return price, name



