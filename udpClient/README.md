# udpClient

```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/udpClient

sudo -E python3 main.py --help
usage: main.py [-h] [--device DEVICE] [--speed SPEED] [--timeout TIMEOUT]
               [--host HOST] --port PORT [--debug]

options:
  -h, --help         show this help message and exit
  --device DEVICE    uart device file name
  --speed SPEED      uart baudrate
  --timeout TIMEOUT  uart timeout
  --host HOST        udp host to connect to
  --port PORT        udp port to connect to
  --debug            enable debug print

# Root privileges are required on Ubuntu/Debian
sudo -E python3 main.py --device /dev/ttyS3 --port 8080

# buildroot does not require root privileges
python3 main.py --device /dev/ttyS3 --port 8080

device=/dev/ttyS3
speed=115200
debug=False
host=255.255.255.255
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

# UDP host address
There are the following four methods for specifying the UDP Address.   

- Limited broadcast address   
 The address represented by 255.255.255.255, or \<broadcast\>, cannot cross the router.   
 Both the sender and receiver must specify a Limited broadcast address.   
 This is default of this example.   

- Directed broadcast address   
 It is possible to cross the router with an address that represents only the last octet as 255, such as 192.168.10.255.   
 Both the sender and receiver must specify the Directed broadcast address.   
 __Note that it is possible to pass through the router.__   

- Multicast address   
 Data is sent to all PCs belonging to a specific group using a special address (224.0.0.0 to 239.255.255.255) called a multicast address.   
 I've never used it, so I don't know anything more.

- Unicast address   
 It is possible to cross the router with an address that specifies all octets, such as 192.168.10.41.   
 Both the sender and receiver must specify the Unicast address.


# Using nDNS
Unfortunately, AT firmware cannot resolve IP addresses using nDNS.   

# UDP server using python
```
#!/usr/bin/python3
# -*- coding : UTF-8 -*-
import time
import select
import socket
import signal
import argparse

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

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('<broadcast>', args.port))
        sock.settimeout(1.0)

        while running:
                try:
                        rmsg, cli_addr = sock.recvfrom(1024)
                        if (type(rmsg) == bytes):
                                rmsg=rmsg.decode('utf-8')
                        print("[{}]".format(rmsg),end="")
                except:
                        #print("timeout")
                        continue

                smsg = ""
                for ch in rmsg:
                        #print("ch={}".format(ch))
                        if ch.islower():
                                smsg = smsg + ch.upper()
                        else:
                                smsg = smsg + ch.lower()

                time.sleep(1)
                print("---->[{}]".format(smsg))
                sock.sendto(smsg.encode(encoding='utf-8'), cli_addr)

        sock.close()
```

