import sys
import os

# Add parent directory to sys.path so Python can find 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sht30 import SHT30

sensor = SHT30(address=0x44)  # or 0x45 if configured differently

temp_c = sensor.get_temperature_celsius()
temp_f = sensor.get_temperature_fahrenheit()
humidity = sensor.get_humidity()

print(f"Temperature: {temp_c:.2f} °C")
print(f"Temperature: {temp_f:.2f} °F")
print(f"Humidity: {humidity:.2f} %RH")