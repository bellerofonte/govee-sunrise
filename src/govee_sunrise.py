import requests
import time
import argparse
import uuid
from config import API_KEY, DEVICE_SKU, DEVICE_MAC  # Import device data from config.py

API_URL = 'https://openapi.api.govee.com/router/api/v1/device/control'
HEADERS = {
    'Govee-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

COLORS = [ 
    14221569, # Deep red
    15663104, # Red - orange
    16384000, # Orange - red
    14500864, # Deep orange
    16337920, # Warm orange
    16739584, # Orange - yellow
    16745984, # Yellow - orange
    16751616, # Deep yellow 
    16758528, # Warm yellow
    16771351, # Warm white
    16771351, # Repeat to ensure it has some time to settle
]

MAX_COLOR_IDX = len(COLORS) - 1

def send_command(capability_type, instance, value):
    '''Send a command to the Govee API with the new request format.'''
    payload = {
        'requestId': str(uuid.uuid4()),
        'payload': {
            'sku': DEVICE_SKU,
            'device': DEVICE_MAC,
            'capability': {
                'type': capability_type,
                'instance': instance,
                'value': value
            }
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def interpolate_color(progress):
    '''Compute smooth color transitions from red to warm white.'''
    index = int(round(progress * MAX_COLOR_IDX))
    return COLORS[index]

def sunrise_emulation(final_brightness, total_time_seconds):
    '''Gradually increases brightness and smoothly transitions color to simulate sunrise.'''
    if final_brightness > 100:
        print('Final brightness cannot exceed 100%. Adjusting to 100%.')
        final_brightness = 100

    brightness_steps = final_brightness
    step_interval = total_time_seconds / brightness_steps

    for i in range(brightness_steps):
        new_brightness = i + 1
        progress = i / brightness_steps
        new_color = interpolate_color(progress)

        start_time = time.time()
        send_command('devices.capabilities.range', 'brightness', new_brightness)
        send_command('devices.capabilities.color', 'colorRgb', new_color)
        execution_time = time.time() - start_time

        adjusted_sleep_time = max(0, step_interval - execution_time)

        print(f'Step {i+1}: Brightness {new_brightness}%, Color {new_color}, Execution Time: {execution_time:.2f}s')
        time.sleep(adjusted_sleep_time)

    print('Sunrise emulation complete!')

def reset_lamp():
    '''Reset lamp to 1% brightness, red color, and turn it off.'''
    send_command('devices.capabilities.range', 'brightness', 1)
    send_command('devices.capabilities.color', 'colorRgb', COLORS[0])
    send_command('devices.capabilities.on_off', 'powerSwitch', 0)
    print('Lamp reset complete!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate a sunrise with Govee Lamp')
    parser.add_argument('final_brightness', type=int, nargs='?', help='Final brightness percentage (1-100)')
    parser.add_argument('total_time_seconds', type=int, nargs='?', help='Total time for sunrise emulation (seconds)')
    parser.add_argument('--reset', action='store_true', help='Reset lamp to 1% brightness, red color, and turn it off')
    
    args = parser.parse_args()
    
    if args.reset:
        reset_lamp()
    else:
        if args.final_brightness is None or args.total_time_seconds is None:
            print('Error: Missing required arguments for sunrise emulation.')
        else:
            sunrise_emulation(args.final_brightness, args.total_time_seconds)
