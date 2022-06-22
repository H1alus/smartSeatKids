import time
# from datetime import timedelta
import logging
import threading
import asyncio
from threading import Event
from fsm import controlMachine
from gps import gps_thread
from ble import ble_thread
from matrix import matrix_thread
from RPi import GPIO

def main():
    #setting logging library
    logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO, 
        format='%(filename)s-%(funcName)s.%(levelname)s: %(message)s at %(relativeCreated)d')
    logging.getLogger('transitions').setLevel(logging.WARNING)

    # set the GPIO thread for auditive/optic allarm
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    # set the gps_thread
    carMoving = Event()
    gps = threading.Thread(target=gps_thread, args=[carMoving])

    # set the ble_thread
    Thigh = Event()
    babyOn = Event()
    ble = threading.Thread(target=ble_thread, args=[Thigh, babyOn])

    # set the matrix_thread
    active = Event()
    alert = Event()   
    matrix = threading.Thread(target=asyncio.run, args=[matrix_thread(active, alert)])

    # start the threads
    gps.start()
    ble.start()
    matrix.start()

    # main Thread is controlMachine
    m = controlMachine(babyOn, carMoving, Thigh, alert, active)
    m.run()

if __name__ == "__main__":
    main()
