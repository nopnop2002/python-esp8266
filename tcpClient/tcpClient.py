#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from esp8266.esp8266 import esp8266

class tcpClient:

	def __init__(self, device, speed, timeout, debug=False):
		self.wifi = esp8266(device, speed, timeout, debug)
		self.debug = debug

	def connect(self, host, port):
		self.host = host
		self.port = port
		ret = self.wifi.sendCommand("ATE0", "OK\r\n")
		if (ret is None):
			print("ATE0 esp8266 not respond")
			return None
		ret = self.wifi.sendCommand("AT+RST", "WIFI GOT IP\r\n")
		if (ret is None):
			print("AT+RST esp8266 not respond")
			return None
		_command = "AT+CIPSTART=\"TCP\",\"{}\",{}".format(host, port)
		_ret = self.wifi.sendCommand(_command, "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if _ret is None:
			print("{} not respond".format(host))
			return False
		_ret = _ret.replace('\r\n', ' ')
		_ret = _ret.replace('OK', '')
		_ret = _ret.replace('"', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.rstrip()
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.split(",")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret[1] != "{}".format(host)):
			print("{} retuned {}".format(host, _ret[1]))
			return False
		if (_ret[2] != "{} CONNECT".format(port)):
			print("{} retuned {}".format(host, _ret[2]))
			return False
		return True

	def send(self, data, size):
		_ret = self.wifi.sendData(data, size, None, 0);
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is "OK"): return True
		return False

	def receive(self):
		_ret = self.wifi.receiveData();
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is None): return [False, 0]
		return [True, _ret]

	def disconnect(self):
		_ret = self.wifi.sendCommand("AT+CIPCLOSE", "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is None): return False
		return True
