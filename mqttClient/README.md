# mqttClient

```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/mqttClient

$ sudo -E python3 publish.py --help
usage: publish.py [-h] [--device DEVICE] [--speed SPEED] [--timeout TIMEOUT] [--host HOST] [--port PORT]
                  [--topic TOPIC] [--payload PAYLOAD] [--qos {0,1,2}] [--debug]

options:
  -h, --help         show this help message and exit
  --device DEVICE    uart device file name
  --speed SPEED      uart baudrate
  --timeout TIMEOUT  uart timeout
  --host HOST        mqtt host to connect to
  --port PORT        mqtt port to connect to
  --topic TOPIC      mqtt topic to publish to
  --payload PAYLOAD  mqtt payload to publish to
  --qos {0,1,2}      mqtt qos to publish to
  --debug            enable debug print

# Root privileges are required on Ubuntu/Debian
sudo -E python3 publish.py --device /dev/ttyS3 --topic /topic/pyserial --payload test

# buildroot does not require root privileges
python3 publish.py --device /dev/ttyS3 --topic /topic/pyserial --payload test

device=/dev/ttyS3
speed=115200
debug=False
host=broker.emqx.io
port=1883
topic=/topic/pyserial
payload=test
qos=0
client.connect = True
client.send = True
client.disconnect = True
```


# MQTT subscribe using mosquitto_sub
```
sudo apt install mosquitto-clients
mosquitto_sub -v -h broker.emqx.io -p 1883  -t "/topic/esp8266"
/topic/esp8266 test
```

