import os
import serial
from serial.tools import list_ports

serialports = []

print('listing com ports...')
ports = list_ports.comports()
print(f'got {len(ports)} ports')
for comport in ports:
  print(f'opening {comport[0]}')
  serialports.append(serial.Serial(comport[0]))

def dispatch_from_ports():
  while True:
    for incomingserial in serialports:
      if incomingserial.in_waiting > 0:
        try:
          serialstr = incomingserial.readline().decode().strip()
          print(serialstr)
        except:
          print('error reading serial. exiting...')
          os._exit(1)

if __name__ == '__main__':
  dispatch_from_ports()
