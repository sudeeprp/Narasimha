import serial
from serial.tools import list_ports

serialports = []

print('listing com ports...')
ports = list_ports.comports()
print(f'got {len(ports)} ports')
for comport in ports:
  print(f'opening {comport[0]}')
  serialports.append(serial.Serial(comport[0]))
