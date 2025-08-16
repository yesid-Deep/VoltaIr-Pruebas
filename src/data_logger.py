import csv
import time
from src.sht30 import SHT30


class DataLogger:
    def __init__(self, sensor=None, interval=2.0, alpha=0.2):
        """
        Initialize the data logger.

        :param sensor: SHT30 instance (if None, create a default one).
        :param interval: Time interval between readings (seconds).
        :param alpha: Smoothing factor for Exponential Moving Average (EMA).
        """
        self.sensor = sensor if sensor else SHT30()
        self.interval = interval
        self.alpha = alpha
        self.ema_temp = 0
        self.ema_hum = 0
        self.sma_window = []
        self.sma_size = 5  # Simple Moving Average window size

    def _apply_filters(self, temp, hum):
        """Apply EMA and SMA filters to temperature and humidity."""

        # Exponential Moving Average (EMA)
        if self.ema_temp == 0:
            self.ema_temp = temp
            self.ema_hum = hum
        else:
            self.ema_temp = self.alpha * temp + (1 - self.alpha) * self.ema_temp
            self.ema_hum = self.alpha * hum + (1 - self.alpha) * self.ema_hum

        # Simple Moving Average (SMA)
        self.sma_window.append((temp, hum))
        if len(self.sma_window) > self.sma_size:
            self.sma_window.pop(0)
        sma_temp = sum([x[0] for x in self.sma_window]) / len(self.sma_window)
        sma_hum = sum([x[1] for x in self.sma_window]) / len(self.sma_window)

        return {
            "raw_temp": temp,
            "raw_hum": hum,
            "ema_temp": self.ema_temp,
            "ema_hum": self.ema_hum,
            "sma_temp": sma_temp,
            "sma_hum": sma_hum
        }

    def capture_data_csv(self, filename="sht30_data.csv", duration=30):
        """
        Capture sensor data at fixed intervals and save to CSV.

        :param filename: CSV file name.
        :param duration: Total capture time in seconds.
        """
        end_time = time.time() + duration

        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp",
                "Temp_C", "Hum_%", 
                "EMA_Temp", "EMA_Hum", 
                "SMA_Temp", "SMA_Hum"
            ])

            while time.time() < end_time:
                temp_c = self.sensor.get_temperature_celsius()
                hum = self.sensor.get_humidity()

                filtered = self._apply_filters(temp_c, hum)

                writer.writerow([
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{filtered['raw_temp']:.2f}",
                    f"{filtered['raw_hum']:.2f}",
                    f"{filtered['ema_temp']:.2f}",
                    f"{filtered['ema_hum']:.2f}",
                    f"{filtered['sma_temp']:.2f}",
                    f"{filtered['sma_hum']:.2f}"
                ])

                print(f"[{time.strftime('%H:%M:%S')}] "
                      f"Raw: {filtered['raw_temp']:.2f}°C / {filtered['raw_hum']:.2f}% | "
                      f"EMA: {filtered['ema_temp']:.2f}°C / {filtered['ema_hum']:.2f}% | "
                      f"SMA: {filtered['sma_temp']:.2f}°C / {filtered['sma_hum']:.2f}%")

                time.sleep(self.interval)
