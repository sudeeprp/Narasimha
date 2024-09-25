from enum import Enum
import threading
import time
from serial_ports import serialports

PillarTalk = Enum('PillarTalk', ['crack', 'fang_kick_peace'])

def serial_write(byte_to_send):
    print(f'writing {byte_to_send}...')
    for outgoingserial in serialports:
        print('...to serial')
        outgoingserial.write(byte_to_send)


def fang_kick_peace():
    def serial_sequence():
        print('starting fang & kick...')
        time.sleep(3)
        serial_write(b'F')
        time.sleep(4)
        serial_write(b'U')
        serial_write(b'K')
        print('...sent fang unfang kick')
        # TODO: Switch the light to lakshmi narasimha
        serial_write(b'R')
    threading.Thread(target=serial_sequence).start()


req_to_pillar = {
    PillarTalk.crack: lambda: serial_write(b'C'),
    PillarTalk.fang_kick_peace: fang_kick_peace
}


def talk_to_pillar(event):
    if event in req_to_pillar:
        req_to_pillar[event]()
