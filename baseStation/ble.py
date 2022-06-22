import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import logging

MAX_TEMP = 40
MIN_TEMP = 4

def inInterval(temperature : float, range=2) -> bool:
    if temperature + range >= MAX_TEMP:
        return True
    elif temperature - range <= MIN_TEMP:
        return True
    else:
        return False

def ble_thread(Thigh, babyOn):
    logging.info('started BLE thread')
    start_time = time.time()
    ble = BLERadio()
    connection = None

    while True:
        if babyOn.is_set():
            babyOn.clear()
        
        if Thigh.is_set():
            Thigh.clear()

        if not connection:
            for adv in ble.start_scan(ProvideServicesAdvertisement):
                name = adv.complete_name
                if not name:
                    continue
                
                if name.strip("\x00") == "CIRCUITPY59a4":
                    if UARTService in adv.services:
                        connection = ble.connect(adv)
                        break
            ble.stop_scan()

        if connection and connection.connected:
            logging.info('connected to bluetooth device')
            uart_service = connection[UARTService]
            babyOn.set() 
            temperature = 0
            summ = 0
            n = 0
            average = 0

            while connection.connected:
                data = uart_service.readline().decode("utf-8").strip()
                try:
                    temperature = float(data)
                except ValueError:
                    logging.error('error in obtaining data from thermistor')
                
                f = open('ble.log', 'a')
                f.write(f'({time.time() - start_time}, {temperature})\n')
                f.close()
                summ += temperature
                if n == 10:
                    average = summ/n
                    summ = 0
                    n = 0
                    if inInterval(average):
                        Thigh.set()
                    elif Thigh.is_set(): 
                        Thigh.clear()
                n += 1
                time.sleep(1)

            connection = None
