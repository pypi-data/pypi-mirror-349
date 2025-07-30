from jvcore import Waker, Communicator
from .porcupine_waker import PorcupineWaker

def getWaker()-> Waker:
    return PorcupineWaker()

def test(comm: Communicator):
    waker = getWaker()
    while True:
        if waker.wakeword_detected():
            print('Wakeword detected')