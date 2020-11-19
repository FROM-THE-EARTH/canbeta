

import time

import pigpio
from pisat.calc import press2alti
from pisat.handler import PigpioI2CHandler
from pisat.sensor import Bme280

import can09.parent.setting as setting


SLEEP_TIME = 0.5        # [sec]


def main():
    pi = pigpio.pi()
    handler = PigpioI2CHandler(pi, setting.I2C_ADDRESS_BME280)
    bme280 = Bme280(handler, name=setting.NAME_BME280)
    
    try:
        while True:
            data = bme280.read()
            if data.press is None or data.temp is None:
                continue
            
            altitude = press2alti(data.press, data.temp)
            print(f"altitude: {altitude} [m]")
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        pass
    
    
if __name__ == "__main__":
    main()
