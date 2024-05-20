#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from esp8266.esp8266 import esp8266

DNS_SERVER1 = "8.8.8.8" # DNS SERVER1
DNS_SERVER2 = "8.8.4.4" # DNS SERVER2
MQTT_KEEP_ALIVE = 60

class mqttClient:

	def __init__(self, device, speed, timeout, debug=False):
		self.wifi = esp8266(device, speed, timeout, debug)
		self.debug = debug

	def connect(self, host, port, qos):
		self.host = host
		self.port = port
		self.pingreq_datetime = datetime.datetime.now()
		self.received = []

		# Get AP info
		_ret = self.wifi.getApInfo()

		# Reset module
		if (_ret is None):
			ret = self.wifi.sendCommand("AT+RST", "WIFI GOT IP\r\n")
			if (ret is None):
				print("AT+RST esp8266 not respond")
				return None

		# Local echo off
		ret = self.wifi.sendCommand("ATE0", "OK\r\n")
		if (ret is None):
			print("ATE0 esp8266 not respond")
			return None

		# Set DNS Server Information
		_ret = self.wifi.setDNS(DNS_SERVER1, DNS_SERVER2)
		if (self.debug): print("_ret=[{}]".format(_ret))

		# Get MAC address
		_mac = self.wifi.getMacInfo()
		_mac = _mac.replace(':','')
		if (self.debug): print("_mac={}".format(_mac))

		# Establish TCP transmission
		_command = "AT+CIPSTART=\"TCP\",\"{}\",{}".format(host, port)
		_ret = self.wifi.sendCommand(_command, "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if _ret is None:
			print("{} not respond".format(host))
			return False
		_ret = _ret.replace('\r\n', '')
		_ret = _ret.replace('OK', '')
		_ret = _ret.replace(' ', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret != "CONNECT"): return False

		# Send CONNECT
		_packetLength = 16 + len(_mac)
		_packet = [0] * _packetLength
		_packet[0] = 0x10 | (qos << 1)
		_packet[1] = _packetLength - 2
		_packet[2] = 0x00
		_packet[3] = 0x06
		_packet[4] = ord('M')
		_packet[5] = ord('Q')
		_packet[6] = ord('I')
		_packet[7] = ord('s')
		_packet[8] = ord('d')
		_packet[9] = ord('p')
		_packet[10] = 0x03
		_packet[11] = 0x02
		_packet[12] = 0x00
		_packet[13] = MQTT_KEEP_ALIVE
		_packet[14] = 0x00
		_packet[15] = len(_mac)
		for _i in range(len(_mac)):
			_packet[_i+16] = ord(_mac[_i])
		if (self.debug): print("_packet={}".format(_packet))
		_ret = self.wifi.sendData(_packet, _packetLength, None, 0, True)
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is not "OK"): return False

		# Wait CONNACK
		_ret = self.wifi.waitData("+IPD,4: \2\0\0")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret == None): return False
		return True

	def publish(self, topic, payload):
		_tlen = len(topic)
		_plen = len(payload)
		_packetLength = 4 + _tlen + _plen
		_packet = [0] * _packetLength
		_packet[0] = 0x30
		_packet[1] = _tlen + _plen + 2
		_packet[2] = 0x00
		_packet[3] = len(topic)
		for _i in range(_tlen):
			_packet[_i+4] = ord(topic[_i])
		for _i in range(_plen):
			_packet[_i+4+_tlen] = ord(payload[_i])
		if (self.debug): print("_packet={}".format(_packet))
		_ret = self.wifi.sendData(_packet, _packetLength, None, 0, True)
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is not "OK"): return False
		return True

	def subscribe(self, topic):
		_tlen = len(topic)
		_packetLength = 7 + _tlen
		_packet = [0] * _packetLength
		_packet[0] = 0x82
		_packet[1] = _tlen + 5
		_packet[2] = 0x00
		_packet[3] = 0x01
		_packet[4] = 0x00
		_packet[5] = _tlen
		for _i in range(_tlen):
			_packet[_i+6] = ord(topic[_i])
		_packet[_tlen+6] = 0
		if (self.debug): print("_packet={}".format(_packet))
		_ret = self.wifi.sendData(_packet, _packetLength, None, 0, True)
		if (self.debug): print("sendData _ret=[{}]".format(_ret))
		if (_ret is not "OK"): return False

		# Wait SUBACK
		_ret = self.wifi.waitData("+IPD,5:\3\0\1\0")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret == None): return False

		self.pingreq_datetime = datetime.datetime.now()
		_ret = self.pingreq()
		if (self.debug): print("pingreq _ret=[{}]".format(_ret))
		return _ret

	def update(self):
		_length = self.wifi.isWaiting()
		if (self.debug): print("_length{}".format(_length))
		if (_length):
			_buffer = self.wifi.readData(_length, binary=True)
			if (self.debug): print("len(_buffer)={}".format(len(_buffer)))
			if (_length != len(_buffer)): return False

			if (self.debug): print("_buffer={}".format(_buffer))
			_ret = self.parsePacket(_buffer)
			if (self.debug): print("_ret={}".format(_ret))
			if (_ret is None): return True
			return _ret

			
		_elasped = datetime.datetime.now() - self.pingreq_datetime
		if (self.debug): print("_elasped=[{}]".format(_elasped.seconds))
		if (_elasped.seconds < MQTT_KEEP_ALIVE): return True
		self.pingreq_datetime = datetime.datetime.now()
		return self.pingreq()

	def parsePacket(self, buffer):
		_length = len(buffer)
		_list = list("\r\n+IPD,")
		_work = buffer[0:7]
		if (self.debug): print("_list{}=".format(_list))
		if (self.debug): print("_work{}=".format(_work))
		if (_list != _work): return None
		
		_totalLength = None
		_payloadLength = None
		for _i in range(7,_length):
			_ch = buffer[_i:_i+1]
			if (self.debug): print("_ch{}={}".format(_i, _ch))
			if (_ch == [':']): 
				_totalLength = buffer[_i+2:_i+3]
				_topicLength = buffer[_i+4:_i+5]
				_body = buffer[_i+5:]
				break
			
		if (_totalLength is None): return None
		if (self.debug): print("_totalLength={}".format(_totalLength))
		if (self.debug): print("_topicLength={}".format(_topicLength))
		if (self.debug): print("_body={}".format(_body))
		_totalLength = _totalLength[0].encode(encoding='utf-8')
		_totalLength = int.from_bytes(_totalLength, 'little')
		if (self.debug): print("_totalLength={}".format(_totalLength))
		_topicLength = _topicLength[0].encode(encoding='utf-8')
		_topicLength = int.from_bytes(_topicLength, 'little')
		if (self.debug): print("_topicLength={}".format(_topicLength))
		_payloadLength = _totalLength - _topicLength - 1
		if (self.debug): print("_payloadLength={}".format(_payloadLength))
		_body = "".join(_body)
		if (self.debug): print("_body={}".format(_body))
		_topic = _body[0:_topicLength]
		_payload = _body[_topicLength:]
		if (self.debug): print("_topic=[{}]".format(_topic))
		if (self.debug): print("_payload=[{}]".format(_payload))
		_received = [_topic, _payload]
		self.received.append(_received)
		if (self.debug): print("_self.received={}".format(self.received))
		return True

	def subscribed(self):
		if (self.debug): print("_self.received={}".format(self.received))
		if (len(self.received) == 0): return None
		_return = self.received
		self.received = []
		return _return

	def pingreq(self):
		# Send PINGREQ
		_packetLength = 2
		_packet = [0] * _packetLength
		_packet[0] = 0xc0
		_packet[1] = 0
		_ret = self.wifi.sendData(_packet, _packetLength, None, 0, True)
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is not "OK"): return False

		# Wait PINGRESP
		_packetLength = 2
		_ret = self.wifi.waitData("+IPD,2:\0")
		if (self.debug): print("waitData _ret=[{}]".format(_ret))
		if (_ret is None): return False
		return True

	def disconnect(self):
		# Send DISCONNECT
		_packetLength = 2
		_packet = [0] * _packetLength
		_packet[0] = 0
		_packet[1] = 0
		_ret = self.wifi.sendData(_packet, _packetLength, None, 0, True)
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is not "OK"): return False

		_ret = self.wifi.waitData("CLOSED\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret == None): return False
		_ret = _ret.replace('\r\n', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret != "CLOSED"): return False

		"""
		_ret = self.wifi.sendCommand("AT+CIPCLOSE", "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is None): return False
		"""

		return True
