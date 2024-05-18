# ntpClient
```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/ntpClient

python3 main.py --help
usage: main.py [-h] [--device DEVICE] [--speed SPEED] [--timeout TIMEOUT] [--host HOST] [--timezone TIMEZONE] [--debug]

options:
  -h, --help           show this help message and exit
  --device DEVICE      uart device file name
  --speed SPEED        uart baudrate
  --timeout TIMEOUT    uart timeout
  --host HOST          time server
  --timezone TIMEZONE  timezone
  --debug              enable debug print

# Root privileges are required on Ubuntu/Debian
sudo -E python3 main.py --device /dev/ttyS3 --timezone 9

# buildroot does not require root privileges
python3 main.py --device /dev/ttyS3 --timezone 9

device=/dev/ttyS3
speed=115200
debug=False
host=time.google.com
timezone=9
client.connect = True
client.sendPacket = True
client.receivePacket = 2024-05-18 22:31:59
```

