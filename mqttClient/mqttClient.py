#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
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

		# Reset module
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

		_ret = self.wifi.waitData("+IPD,4:")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret == None): return False
		_ret = _ret.replace('\r\n', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret != "+IPD,4:"): return False
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

	def subscribe(self):
		_ret = self.wifi.receiveData();
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is None): return [False, 0]
		return [True, _ret]

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
