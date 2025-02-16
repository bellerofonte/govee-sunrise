import requests
from config import API_KEY  # Import device data from config.py

API_URL = 'https://openapi.api.govee.com/router/api/v1/user/devices'
HEADERS = {
    'Govee-API-Key': API_KEY
}

if __name__ == '__main__':
    response = requests.get(API_URL, headers=HEADERS)
    res = response.json()
    if 'data' not in res:
        print('Error: No device data found in the response.')
        print(res)
        exit(1)

    for device in res['data']:
        if 'type' not in device:
            continue

        if device['type'] != 'devices.types.light':
            continue
        
        sku = device['sku'] if 'sku' in device else 'Unknown'
        mac = device['device'] if 'device' in device else 'Unknown'
        print(f'Device SKU: "{sku}", MAC: "{mac}"')
