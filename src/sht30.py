import smbus
import time

class SHT30:
    def __init__(self, address=0x44, bus=1):
        """
        Initialize the SHT30 sensor.
        
        :param address: I2C address of the sensor (default 0x44).
        :param bus: I2C bus number (default 1 for Raspberry Pi).
        """
        self.address = address
        self.bus = smbus.SMBus(bus)

    def _read_sensor(self):
        """
        Send measurement command and read raw data from SHT30.
        :return: list of 6 bytes [T_MSB, T_LSB, T_CRC, H_MSB, H_LSB, H_CRC]
        """
        # Trigger measurement (high repeatability, clock stretching disabled)
        self.bus.write_i2c_block_data(self.address, 0x2C, [0x06])
        time.sleep(0.015)  # wait for measurement (~15 ms)

        # Read 6 bytes of data
        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)
        return data

    def get_temperature_celsius(self):
        """
        Read and return temperature in Celsius.
        """
        data = self._read_sensor()
        raw_temp = data[0] << 8 | data[1]
        c_temp = -45 + (175 * (raw_temp / 65535.0))
        return c_temp

    def get_temperature_fahrenheit(self):
        """
        Read and return temperature in Fahrenheit.
        """
        c_temp = self.get_temperature_celsius()
        return c_temp * 1.8 + 32

    def get_humidity(self):
        """
        Read and return relative humidity in %.
        """
        data = self._read_sensor()
        raw_hum = data[3] << 8 | data[4]
        humidity = 100 * (raw_hum / 65535.0)
        return humidity
