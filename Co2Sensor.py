from machine import Pin, ADC
import time
import dht  # Import DHT11 library

# Pins used by sensors
co2_sensor = ADC(Pin(26))  # Air quality sensor (CO2)
temp_sensor = dht.DHT11(Pin(17))  # DHT11 sensor

# Pins used by LEDs
greenLed = Pin(15, Pin.OUT)
yellowLed = Pin(14, Pin.OUT)
redLed = Pin(13, Pin.OUT)

# CO2 compliance levels (voltage approximation)
NORMAL_READING = 1.25  # Example threshold for good air quality
MIDDLE_READING = 1.4   # Moderate CO2 level
HIGH_READING = 1.5     # High CO2 level (needs ventilation)

CONVERSION_FACTOR = 3.3 / 65535  # Convert raw ADC to voltage

while True:
    try:
        # Read DHT11 sensor data
        temp_sensor.measure()  # Trigger reading
        temperature = temp_sensor.temperature()  # Read temperature (°C)
        humidity = temp_sensor.humidity()  # Read humidity (%)
        
        # Read CO2 sensor voltage
        co2_voltage = co2_sensor.read_u16() * CONVERSION_FACTOR
        
        # Map voltage to estimated PPM values (example values, adjust as needed)
        co2_ppm = co2_voltage * 1000  # Simplified conversion
        
        # LED logic based on CO2 levels
        if co2_voltage <= MIDDLE_READING:
            greenLed.value(1)
            yellowLed.value(0)
            redLed.value(0)
            status = "Good air quality"
        elif MIDDLE_READING < co2_voltage <= HIGH_READING:
            greenLed.value(0)
            yellowLed.value(1)
            redLed.value(0)
            status = "Moderate CO2, consider ventilation"
        else:
            greenLed.value(0)
            yellowLed.value(0)
            redLed.value(1)
            status = "High CO2! Ventilate the room"

        # Print sensor readings
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%, CO2: {co2_ppm} PPM - {status}")

    except Exception as e:
        print("Sensor error:", e)

    time.sleep(2)  # Delay before next reading
