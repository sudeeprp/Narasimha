import os
from doer import Doer
from serial_ports import serialports
from story import incoming
import player
import pillar_talk

def dispatch_from_ports():
  doer = Doer(player.play, pillar_talk.send_to_serial)
  while True:
    for incomingserial in serialports:
      if incomingserial.in_waiting > 0:
        try:
          serialstr = incomingserial.readline().decode().strip()
          print(serialstr)
          doer.do(incoming(serialstr))
        except:
          print('error reading serial. exiting...')
          os._exit(1)


if __name__ == '__main__':
  dispatch_from_ports()
