from transitions import Machine
from transitions.extensions import GraphMachine
from threading import Event

babyOn = Event()
elTime = 0
carMoving = Event()
Thigh = Event()
BabyIsOn = lambda :  babyOn.is_set()
notBabyOn = lambda : not babyOn.is_set()
setStateAlarm = lambda : True if elTime >= 60 else False
CarIsMoving = lambda : carMoving.is_set()
notCarMoving = lambda : not carMoving.is_set()
TIsHigh = lambda : Thigh.is_set()

# return to default if the baby is not placed
states = ['default', 'baby_set', 'alarm', 'car_moving', 'car_stopped']
transitions = [
        {'trigger' : 'update', 'source': '*', 'dest': 'default', 'conditions' : 'notBabyOn'},
        {'trigger' : 'update', 'source' : 'default', 'dest' : 'baby_set', 'conditions' : 'BabyIsOn'},
        {'trigger' : 'update', 'source' : 'baby_set', 'dest' : 'alarm', 'conditions' : 'setStateAlarm'},
        {'trigger' : 'update', 'source' : 'baby_set', 'dest' : 'car_moving', 'conditions' : 'CarIsMoving'},
        {'trigger' : 'update', 'source' : 'car_moving', 'dest' : 'car_stopped', 'conditions' : 'notCarMoving'},
        {'trigger' : 'update', 'source' : 'car_stopped', 'dest' : 'car_moving', 'conditions' : 'CarIsMoving'},
        {'trigger' : 'update', 'source' : 'car_stopped', 'dest' : 'alarm', 'conditions' : 'setStateAlarm'}, 
        {'trigger' : 'update', 'source' : 'car_stopped', 'dest' : 'alarm', 'conditions' : 'TIsHigh'}
    ]

m = GraphMachine(states=states, transitions=transitions, initial='default', show_conditions=True)
m.get_graph().draw('my_state_diagram.png', prog='dot')