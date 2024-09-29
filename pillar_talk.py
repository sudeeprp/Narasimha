from enum import Enum
import threading
import time
from serial_ports import serialports
from player import play, PlayerEvents

PillarTalk = Enum('PillarTalk', ['first_hit', 'crack', 'fang_kick_peace'])

def serial_write(byte_to_send):
    print(f'writing {byte_to_send}...')
    for outgoingserial in serialports:
        print('...to serial')
        outgoingserial.write(byte_to_send)


def first_hit(done):
    play(PlayerEvents.first_hit, done)


def crack(done):
    serial_write(b'C')
    play(PlayerEvents.crack, done)


def fang_kick_peace(done):
    # These functions are declared in reverse order of occurrence
    def reset():
        print('reset')
        serial_write(b'R')
        done()
    def simha():
        print('Lakshminarasimha')
        # TODO: Switch the light to lakshmi narasimha
        play(PlayerEvents.simha, reset)
    def sharanam():
        print('sharanam')
        play(PlayerEvents.sharanam, simha)
        serial_write(b'U')
    def unfang_and_kick():
        print('wait, unfang and kick')
        time.sleep(4)
        serial_write(b'U')
        serial_write(b'K')
        play(PlayerEvents.kick, sharanam)
    def fang(count=0):
        if count < 6:
            if count % 2 == 0:
                time.sleep(0.25)
                serial_write(b'F')
                play(PlayerEvents.fang, lambda: fang(count + 1))
            else:
                time.sleep(1)
                serial_write(b'U')
                fang(count + 1)
        else:
            unfang_and_kick()
    def serial_sequence():
        print('starting fang...')
        time.sleep(3) # wait for placement to finish and audience to take back hand
        fang(0)
    threading.Thread(target=serial_sequence).start()


req_to_pillar = {
    PillarTalk.first_hit: first_hit,
    PillarTalk.crack: crack,
    PillarTalk.fang_kick_peace: fang_kick_peace
}


def request_pillar(event, done):
    if event in req_to_pillar:
        req_to_pillar[event](done)
