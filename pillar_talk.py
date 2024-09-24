from enum import Enum
from serial_ports import serialports

PillarTalk = Enum('PillarTalk', ['crack'])

req_to_pillar = {
    PillarTalk.crack: 'C'
}

def serial_write(byte_to_send):
    for outgoingserial in serialports:
        outgoingserial.write(byte_to_send)


def send_to_serial(event):
    if event in req_to_pillar:
        serial_write(req_to_pillar[event].encode('utf-8'))


if __name__ == '__main__':
    while True:
        to_send = input()
        serial_write(to_send.encode('utf-8'))
