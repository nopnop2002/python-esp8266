# python-esp8266   
Network example using esp8266 AT firmware.   
You don't need Ethernet card.   
You need only pyserial library and ESP8266 module.   

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

# How to use
```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/connectWiFi

# Know your UART device   
ls /dev/tty*
/dev/tty  /dev/ttyFIQ0  /dev/ttyS3  /dev/ttyS4

# Root privileges are required on Ubuntu/Debian
sudo -E python3 main.py --device /dev/ttyS3

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

