# python-esp8266   
Network example using esp8266 AT firmware.   
You don't need Ethernet card.   
You need only pyserial library and ESP8266 module.   

# Background   
I recently bought a LuxkFox Pico Mini board.   
It's a very small Linux board.   
buildroot linux works.   
But there is no network.   
So, I made it to use the network with this board.

![ProMini-1](https://github.com/nopnop2002/python-esp8266/assets/6020549/f822d021-d73b-46b0-9485-0b324dbce3e9)

# Hardware requirements   
ESP8266 module like ESP01   

# Software requirements   
- pysirail library   
In your buildroot environment you can enable it with this.   
![buildroot-71](https://github.com/nopnop2002/python-esp8266/assets/6020549/2b3be767-83e3-4d4c-8d28-93303196fca2)

- ESP8266 AT Firmware   
 You can download from [here](https://github.com/espressif/ESP8266_NONOS_SDK/tags).   
 Some versions do not support 1M SoCs like ESP01.   

# Flash AT firmware to ESP01.   
The 3.3V output of the UART-USB converter has too little current to be used.   
Power is supplied using 5V from the UART-USB converter and 3.3V from the regulator.   
- GPIO2 must be pulled up.   
- GPIO0 must be connected to GND.   
- CH_PD must be pulled up.   
- RESET must be pulled up.   

Click [here](https://github.com/nopnop2002/Arduino-ESPAT-TCP/tree/master/Flash_AT_firmware) for details.

![esp01-flash](https://user-images.githubusercontent.com/6020549/33159146-b8456238-d053-11e7-8202-a86cca2f8a3d.jpg)


# Setup ESP01 using terminal software such as CoolTerm.   
- GPIO2 must be pulled up.   
- GPIO0 must be pulled up.   
- CH_PD must be pulled up.   
- RESET must be pulled up.   

![esp01-setup](https://user-images.githubusercontent.com/6020549/33159150-bdade984-d053-11e7-9b93-bbbf05573441.jpg)

Connect to ESP01 at 115200 bps using terminal software.   

```
AT+GMR
AT version:1.6.2.0(Apr 13 2018 11:10:59)
SDK version:2.2.1(6ab97e9)
compile time:Jun  7 2018 19:34:26
Bin version(Wroom 02):1.6.2
OK

AT+CWMODE=1

OK
AT+CWLAP
+CWLAP:(3,"Picking",-86,"34:12:98:08:4b:4a",1,-4)
+CWLAP:(4,"ctc-g-fa4a2e",-92,"c0:25:a2:b1:8c:2e",2,3)
+CWLAP:(4,"aterm-e625c0-g",-49,"c0:25:a2:ac:cb:ba",3,15)
+CWLAP:(1,"aterm-e625c0-gw",-48,"c2:25:a2:ac:cb:ba",3,15)

OK

AT+CWJAP="Your AP's SSID","Your AP's password"
WIFI CONNECTED
WIFI GOT IP

OK

AT+CIPSTA?
+CIPSTA:ip:"192.168.10.142"
+CIPSTA:gateway:"192.168.10.1"
+CIPSTA:netmask:"255.255.255.0"

OK
AT+CWQAP

OK
```

AT firmware has a function that automatically connects to the last connected AP when the module is reset.   
Using this function, you can omit the SSID and password.   

```
AT+RST
WIFI CONNECTED
WIFI GOT IP
AT+CIPSTA?
+CIPSTA:ip:"192.168.10.142"
+CIPSTA:gateway:"192.168.10.1"
+CIPSTA:netmask:"255.255.255.0"

OK
```

If you want to change the AP, execute the following command again.   
```
AT+CWJAP="New AP's SSID","New AP's password"
WIFI CONNECTED
WIFI GOT IP
```

# How to Firmware Upate

1.Make sure TE(terminal equipment) is in sta mode   
```
AT+CWMODE=1

OK
```

2.Make sure TE got ip address   
```
AT+CIPSTA?
+CIPSTA:ip:"192.168.10.115"
+CIPSTA:gateway:"192.168.10.1"
+CIPSTA:netmask:"255.255.255.0"

OK
```

3.Let's update   
```
AT+CIUPDATE
+CIPUPDATE:1    found server
+CIPUPDATE:2    connect server
+CIPUPDATE:3    got edition
+CIPUPDATE:4    start start

OK
```

4.Check firmware version   
```
AT+GMR
AT version:1.7.5.0(Oct 20 2021 19:14:04)
SDK version:3.0.5(b29dcd3)
compile time:Oct 20 2021 20:13:50
Bin version(Wroom 02):1.7.5
OK
```

# Connect ESP01 to HOST   
- ESP01(Tx)  - UART-RX port of host   
- ESP01(Rx)  - UART-TX port of host   
- ESP01(Gnd) - Gnd of host   
- ESP01(3v3) - 3V3 of host(*1)   

(*1) It is necessary to be able to supply sufficient current.

# How to use in Ubuntu/Debian environment   
```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/connectWiFi

# Know your UART device   
ls /dev/tty*
/dev/tty  /dev/ttyFIQ0  /dev/ttyS3  /dev/ttyS4

# Root privileges are required on Ubuntu/Debian
sudo -E python3 main.py --device /dev/ttyS3

device=/dev/ttyS3
speed=115200
debug=False
ip=['192.168.10.108', '192.168.10.1', '192.168.10.1']
mac=5c:cf:7f:6b:00:1b
```

# Transfer file using RNDIS functionality   
In a environment that does not have a network support, files are transferred using the RNDIS function.   
Ubuntu 20.04/Debian 11 is required as the RNDIS server.   
In the Ubuntu 22.04/Debian 12 environment, the usb0 interface has been changed to a "consistent network device naming method".   

Clone to RNDIS server.
```
git clone https://github.com/nopnop2002/python-esp8266
```

When power is supplied to the RNDIS client from the Ubuntu/Dibian machine, the USB0 interface will be displayed on the Ubuntu/Debian side as shown below.   
```
$ sudo ifconfig usb0
usb0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::a742:1ab5:c616:d016  prefixlen 64  scopeid 0x20<link>
        ether 7a:da:62:7c:d5:bb  txqueuelen 1000  (Ethernet)
        RX packets 21  bytes 2169 (2.1 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 39  bytes 8001 (8.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ nmcli conn show
NAME        UUID                                  TYPE      DEVICE
Wired connection 2  ea035181-2f58-3f41-bf2b-89c5022bb4e0  ethernet  usb0
Wired connection 1  5bfff474-56e9-3a46-81d7-3b3a7d5692d7  ethernet  enp4s0
```

Assign a fixed IP address to usb0 interface using the nmcli command.
The fixed IP address assigned to the Ubuntu/Debian side can be any as long as it is in the same segment as the RNDIS client board.
```
$ sudo nmcli connection down "Wired connection 2"
$ sudo nmcli connection modify "Wired connection 2" ipv4.addresses "172.32.0.100/16"
$ sudo nmcli connection modify "Wired connection 2" ipv4.method manual
$ sudo nmcli connection up "Wired connection 2"
$ nmcli device show usb0
GENERAL.DEVICE:                         usb0
GENERAL.TYPE:                           ethernet
GENERAL.HWADDR:                         DA:1F:7F:84:10:69
GENERAL.MTU:                            1500
GENERAL.STATE:                          100 (connected)
GENERAL.CONNECTION:                     Wired connection 2
GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/6
WIRED-PROPERTIES.CARRIER:               ƒIƒ“
IP4.ADDRESS[1]:                         172.32.0.100/16
IP4.GATEWAY:                            --
IP4.ROUTE[1]:                           dst = 172.32.0.0/16, nh = 0.0.0.0, mt = 101
IP6.ADDRESS[1]:                         fe80::f220:3c47:db11:8fbe/64
IP6.GATEWAY:                            --
IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 101
```

Check the result with ifconfig.
```
$ sudo ifconfig usb0
usb0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.32.0.100  netmask 255.255.0.0  broadcast 172.32.255.255
        inet6 fe80::f220:3c47:db11:8fbe  prefixlen 64  scopeid 0x20<link>
        ether da:1f:7f:84:10:69  txqueuelen 1000  (Ethernet)
        RX packets 53  bytes 7107 (7.1 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 109  bytes 19284 (19.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Now you can ping the RNDIS client and use ssh and scp.
```
$ ping 173.32.0.93
PING 173.32.0.93 (192.168.10.45) 56(84) bytes of data.
64 bytes from 192.168.10.45: icmp_seq=1 ttl=64 time=0.607 ms
64 bytes from 192.168.10.45: icmp_seq=2 ttl=64 time=0.365 ms
64 bytes from 192.168.10.45: icmp_seq=3 ttl=64 time=0.268 ms
64 bytes from 192.168.10.45: icmp_seq=4 ttl=64 time=0.373 ms
^C
--- 173.32.0.93 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3059ms
rtt min/avg/max/mdev = 0.268/0.403/0.607/0.124 ms

$ scp -r python-esp8266 root@172.32.0.93:/root
root@172.32.0.93's password:
```

# How to use in buildroot environment   
```
cd python-esp8266/connectWiFi

# Know your UART device   
ls /dev/tty*
/dev/tty  /dev/ttyFIQ0  /dev/ttyS3  /dev/ttyS4

# buildroot does not require root privileges
python3 main.py --device /dev/ttyS3

device=/dev/ttyS3
speed=115200
debug=False
ip=['192.168.10.108', '192.168.10.1', '192.168.10.1']
mac=5c:cf:7f:6b:00:1b
```

# UART to WiFi module   
We can get a module for UART communication.   
We can write AT firmware to this.   
![ESP-UART-MODULE-1](https://user-images.githubusercontent.com/6020549/104827197-b504cd80-589e-11eb-95a8-f12c75670ced.JPG)

![ESP-UART-MODULE-2](https://user-images.githubusercontent.com/6020549/104827200-b8985480-589e-11eb-9a01-e70d4fbd55cc.JPG)

