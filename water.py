import RPi.GPIO as GPIO
import requests
import json

# Moisture sensor pin
moisture_sensor_pin = 17

# Water pump pin
water_pump_pin = 18

# Weather API key
weather_api_key = "YOUR_API_KEY"

# Location for weather forecast
location = "YOUR_LOCATION"

# Minimum moisture level before watering
min_moisture = 600

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_sensor_pin, GPIO.IN)
GPIO.setup(water_pump_pin, GPIO.OUT)

def check_moisture():
	moisture = GPIO.input(moisture_sensor_pin)
    if moisture < min_moisture:
        return True
    else:
        return False

def check_forecast():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={weather_api_key}"
    r = requests.get(url)
    data = json.loads(r.text)
    forecast = data["list"][0]["weather"][0]["main"]
    if forecast != "Rain":
        return True
    else:
        return False

def water_plants():
    if check_moisture() and check_forecast():
        GPIO.output(water_pump_pin, True)
        print("Watering plants")
    else:
        GPIO.output(water_pump_pin, False)
        print("Not watering plants")

while True:
    water_plants()
    time.sleep(3600) # check every hour
