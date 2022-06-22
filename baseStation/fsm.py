from transitions import Machine, MachineError
import time
import logging
from RPi import GPIO
from transitions.extensions import GraphMachine

class controlMachine:
    def __init__(self, babyOn, carMoving, Thigh, alert, active):
        self.babyOn = babyOn
        self.carMoving = carMoving
        self.Thigh = Thigh
        self.elTime = 0
        self.alert = alert
        self.active = active

        self.BabyIsOn = lambda : self.babyOn.is_set()
        self.notBabyOn = lambda : not self.babyOn.is_set()
        self.setStateAlarm = lambda : True if self.elTime >= 120 else False
        self.CarIsMoving = lambda : self.carMoving.is_set()
        self.notCarMoving = lambda : not self.carMoving.is_set()
        self.TIsHigh = lambda : self.Thigh.is_set()

        states = ['default', 'baby_set', 'alarm', 'car_moving', 'car_stopped']
        self.countstates = ['baby_set', 'alarm', 'car_stopped']
        transitions = [
            {'trigger' : 'update', 'source': states[1::], 'dest': 'default', 'conditions' : 'notBabyOn', 'after': 'defaultOut'},
            {'trigger' : 'update', 'source' : 'default', 'dest' : 'baby_set', 'conditions' : 'BabyIsOn', 'before' : 'activeSet', 'after' : 'baby_setOut'},
            {'trigger' : 'update', 'source' : 'baby_set', 'dest' : 'alarm', 'conditions' : 'setStateAlarm', 'after': 'alarmOut'},
            {'trigger' : 'update', 'source' : 'baby_set', 'dest' : 'car_moving', 'conditions' : 'CarIsMoving', 'after': 'car_movingOut'},
            {'trigger' : 'update', 'source' : 'car_moving', 'dest' : 'car_stopped', 'conditions' : 'notCarMoving', 'after': 'car_stoppedOut'},
            {'trigger' : 'update', 'source' : 'car_stopped', 'dest' : 'car_moving', 'conditions' : 'CarIsMoving', 'after': 'car_movingOut'},
            {'trigger' : 'update', 'source' : 'car_stopped', 'dest' : 'alarm', 'conditions' : 'setStateAlarm', 'after': 'alarmOut'}, 
            {'trigger' : 'update', 'source' : 'car_stopped', 'dest' : 'alarm', 'conditions' : 'TIsHigh', 'after': 'alarmOut'},
            {'trigger' : 'update', 'source' : 'alarm', 'dest' : 'car_moving', 'conditions' : 'CarIsMoving', 'after': 'car_movingOut'}
        ]
        m = Machine(model=self, states=states, transitions=transitions, initial='default')
        # m = GraphMachine(model=self, states=states, transitions=transitions, initial='default', show_conditions=True)

    def activeSet(self):
        self.active.set()

    def defaultOut(self):
        logging.info('state = default')
        GPIO.output(17, GPIO.LOW)
        if self.alert.is_set():
            self.alert.clear()


    def baby_setOut(self):
        logging.info('state = baby_set')
        GPIO.output(17, GPIO.LOW) 
        if self.alert.is_set():
            self.alert.clear()
    
    def alarmOut(self):
        logging.info('state = alarm')
        GPIO.output(17, GPIO.HIGH)
        if not self.alert.is_set():
            self.alert.set()

    
    def car_movingOut(self):
        logging.info('state = car_moving')
        GPIO.output(17, GPIO.LOW)
        if self.alert.is_set():
            self.alert.clear()
        
    def car_stoppedOut(self):
        logging.info('state = car_stopped')
        GPIO.output(17, GPIO.LOW) 
        if self.alert.is_set():
            self.alert.clear()

    def _countElTime(self):
        if self.state in self.countstates:
            self.elTime += 1
        else:
            if self.elTime != 0:
                self.elTime = 0
    
    def run(self):
        while True:
            try:
                self.update()
            except MachineError:
                logging.error('encountered machine error')
                self.m.set_state('default')
            
            self._countElTime()
            time.sleep(1)

if __name__ == '__main__':
    m = controlMachine(None, None, None, None, None)
    m.get_graph().draw('my_state_diagram.png', prog='dot')
