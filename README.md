# govee-sunrise

Realistic sunrise emilation for Govee lamps

### Preparation

#### 1. Install dependencies

```sh
python -m pip install -r requirements.txt
```

#### 2. Obtain Govee API key

In the Govee app, go to `Settings` > `Apply for API Key`, and once it is received via email, create a file `config.py` and copy the API key to it:

```python
# src/config.py
API_KEY = "YOUR_API_KEY"
```

#### 3. Obtain Govee device SKU and MAC

Use `govee_get_devices.py` to get the SKU and MAC of your device:

```sh
python src/govee_get_devices.py
```

Sample output:

```
Device SKU: "H6022", MAC: "00:11:22:33:44:55:66:77"
```

Copy the SKU and MAC to `config.py`:

```python
# src/config.py
API_KEY = "YOUR_API_KEY"
DEVICE_SKU = "H6022"
DEVICE_MAC = "00:11:22:33:44:55:66:77"
```

#### 4. Run the script

First, reset the device to default state - is to be done every evening before going to sleep to prevent turning device on with wrong color or brightness on the next morning. That is because Govee does not provide a way to adjust both brightness and color at the same time

```sh
python src/govee_sunrise.py --reset
```

Then, run the script to emulate sunrise with the target brightness (in percents) and duration (in seconds):

```sh
python src/govee_sunrise.py 80 900
```

Is is suppesed to be run via `cron`, e.g. every morning at the time you want the sunrise to start.
