# circuit playground should do minimal signal elaboration and send data harvested from various sensors
import time
import board
import analogio
import adafruit_thermistor
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

import _bleio

#global parameters initialization
analogIn = analogio.AnalogIn(board.A1)
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)

# checks whether the baby is inside the vehicle or not
def babyOn():
    voltageIn = (analogIn.value * 3.3) / 65536
    if voltageIn > 0.5:
        return True
    else:
        return False


def main():
    print(_bleio.adapter.address)
    ble = BLERadio()
    uart_server = UARTService()
    advertisement = ProvideServicesAdvertisement(uart_server)

    while True:

        # ble connect only if the baby is in the vehicle
        if babyOn():
            # Advertise when not connected.
            ble.start_advertising(advertisement)
            while not ble.connected:
                print('not connected')
                time.sleep(1)

            ble.stop_advertising()
            # takes the first connection possible into account 
            # since it's the only one we can establish
            try:
               conn = ble.connections[0]
            except:
                conn = None
            #while we are connected transmit the data
            while ble.connected and babyOn():               
                temperature = thermistor.temperature
                print(f'{temperature}')
                uart_server.write(f"{temperature}\n")
                time.sleep(1)
                
            time.sleep(1)
            conn.disconnect()
        time.sleep(2)

if __name__ == "__main__":
    main()
    