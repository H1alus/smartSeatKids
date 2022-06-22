from math import radians, cos, sin, asin, sqrt
import serial
import time
import pynmea2
import logging

def geoDistance(lastLat, lat, lastLng, lng) -> float:
    lat = radians(lat)
    lng = radians(lng)
    lastLat = radians(lastLat)
    lastLng = radians(lastLng)  
    # Haversine formula
    dlat = lat - lastLat
    dlng = lng - lastLng
    a = sin(dlat / 2)**2 + cos(lastLat) * cos(lat) * sin(dlng / 2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in meters
    r = 6371000
    distance = c * r
    return distance

def gps_thread(carMoving, updateRate=20):
    logging.info('started gps thread')
    start_time = time.time()
    lastLat = 0
    carMoving.clear()
    lastLng = 0
    while True:
        #sets interfaces and pynmea2
        port="/dev/ttyACM0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        data = ser.readline()
        #try to decode the bytes from GPS in to a UTF-8 string
        #if not decodable data is not relevant so sringdata will be empty
        try:
            stringdata = data.decode('utf-8')
        except UnicodeDecodeError:
            logging.error('error decoding data from GPS')
            stringdata = str()
        
        # gets lat and lng from GPRMC data
        if stringdata[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(stringdata)

            if lastLat == 0 and lastLng == 0:
                lastLat = newmsg.latitude
                lastLng = newmsg.longitude
            
            else:
                lat = newmsg.latitude
                lng = newmsg.longitude
                distance = geoDistance(lat, lastLat, lng, lastLng)
                f = open('gps.log', 'a')
                f.write(f'({time.time() - start_time}, {distance})\n')
                f.close()
                if distance >= 50:
                    if not carMoving.is_set():
                        carMoving.set()
                elif carMoving.is_set():
                    carMoving.clear()

                lastLat = lat
                lastLng = lng
                time.sleep(updateRate)



