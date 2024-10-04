import os
from doer import Doer
from player import stop_playing
from serial_ports import serialports
from story import incoming
import pillar_talk
import serial
from serial.tools import list_ports
import msvcrt

last_serialstr = ''
serial_repeats = 0


def printlog(serialstr):
  global last_serialstr, serial_repeats
  if serialstr == last_serialstr:
    serial_repeats += 1
  else:
    serial_repeats = 1
  if serial_repeats == 1:
    print(f'\n{serialstr}', end='')
  else:
    print(f'\r{serialstr} x {serial_repeats} ', end='')
  last_serialstr = serialstr


def respond_to_key():
  if msvcrt.kbhit():
      key = msvcrt.getch()
      if key == b'q':
        print('got q for exit...')
        stop_playing()
        exit(0)
      elif key == b'w':
        print('got w for low power mode...')
        pillar_talk.request_pillar(pillar_talk.PillarTalk.low_power, lambda: True)
      elif key == b'e':
        print('got e to get back on...')
        pillar_talk.request_pillar(pillar_talk.PillarTalk.back_on, lambda: True)


def dispatch_from_ports():
  doer = Doer(pillar_talk.request_pillar)
  while True:
    for incomingserial in serialports:
      if incomingserial.in_waiting > 0:
        try:
          serialstr = incomingserial.readline().decode().strip()
        except:
          print('error reading serial. exiting...')
          os._exit(1)
        printlog(serialstr)
        doer.do(incoming(serialstr))
    respond_to_key()

if __name__ == '__main__':
  print('listing com ports...')
  ports = list_ports.comports()
  print(f'got {len(ports)} ports')
  for comport in ports:
    print(f'opening {comport[0]}')
    serialports.append(serial.Serial(comport[0]))
  print('start dispatch...')
  dispatch_from_ports()
