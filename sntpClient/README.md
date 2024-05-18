# sntpClient
```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/sntpClient

python3 main.py --help
usage: main.py [-h] [--device DEVICE] [--speed SPEED] [--timeout TIMEOUT]
               [--timezone TIMEZONE] [--debug]

options:
  -h, --help           show this help message and exit
  --device DEVICE      uart device file name
  --speed SPEED        uart baudrate
  --timeout TIMEOUT    uart timeout
  --timezone TIMEZONE  timezone
  --debug              enable debug print

# Root privileges are required on Ubuntu/Debian
sudo -E python3 main.py --device /dev/ttyS3 --timezone 9

# buildroot does not require root privileges
python3 main.py --device /dev/ttyS3 --timezone 9

device=/dev/ttyS3
speed=115200
debug=False
dns=['8.8.8.8', '8.8.4.4']
datetime is [Sat May 18 11:42:06 2024]
```

