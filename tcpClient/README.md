# tcpClient

```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/tcpClient

sudo -E python3 main.py --help
usage: main.py [-h] [--device DEVICE] [--speed SPEED] [--timeout TIMEOUT]
               --host HOST --port PORT [--debug]

options:
  -h, --help         show this help message and exit
  --device DEVICE    uart device file name
  --speed SPEED      uart baudrate
  --timeout TIMEOUT  uart timeout
  --host HOST        tcp host to connect to
  --port PORT        tcp port to connect to
  --debug            enable debug print

# Root privileges are required on Ubuntu/Debian
sudo -E python3 main.py --device /dev/ttyS3 --host 192.168.10.46 --port 8080

# buildroot does not require root privileges
python3 main.py --device /dev/ttyS3 --host 192.168.10.46 --port 8080

device=/dev/ttyS3
speed=115200
debug=False
host=192.168.10.46
port=8080
client.connect = True
client.send = True
client.receive = [True, 'hELLO! wORLD! 0']
client.send = True
client.receive = [True, 'hELLO! wORLD! 1']
client.send = True
client.receive = [True, 'hELLO! wORLD! 2']
client.send = True
client.receive = [True, 'hELLO! wORLD! 3']
client.send = True
client.receive = [True, 'hELLO! wORLD! 4']
client.send = True
client.receive = [True, 'hELLO! wORLD! 5']
client.send = True
client.receive = [True, 'hELLO! wORLD! 6']
client.send = True
client.receive = [True, 'hELLO! wORLD! 7']
client.send = True
client.receive = [True, 'hELLO! wORLD! 8']
client.send = True
client.receive = [True, 'hELLO! wORLD! 9']
client.disconnect = True
```
# Using nDNS
Unfortunately, AT firmware cannot resolve IP addresses using nDNS.   

# TCP server using python
```
#!/usr/bin/python3
# -*- coding : UTF-8 -*-
import socket
#!/usr/bin/python3
# -*- coding : UTF-8 -*-
import socket
import signal
import argparse
server_ip = "0.0.0.0"

def handler(signal, frame):
    global running
    print('handler')
    running = False

if __name__=='__main__':
    signal.signal(signal.SIGINT, handler)
    running = True

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='tcp port', default=8080)
    args = parser.parse_args()
    print("port={}".format(args.port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server_ip, args.port))

    while True:
        sock.listen(5)
        sock.settimeout(1.0)
        try:
            client,address = sock.accept()
            print("Connected!! [ Source : {}]".format(address))
        except:
            #print("Timeout. running={}".format(running))
            if running is False: break
            continue

        while running:
            rmsg = client.recv(1024)
            print("len(rmsg)={}".format(len(rmsg)))
            if (len(rmsg) == 0): break
            if (type(rmsg) == bytes):
                rmsg=rmsg.decode('utf-8')
            print("[{}]".format(rmsg),end="")

            smsg = ""
            for ch in rmsg:
                #print("ch={}".format(ch))
                if ch.islower():
                    smsg = smsg + ch.upper()
                else:
                    smsg = smsg + ch.lower()

            print("---->[{}]".format(smsg))
            client.send(smsg.encode(encoding='utf-8'))

        client.close()
```

