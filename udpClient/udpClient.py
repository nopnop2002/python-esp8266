#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from esp8266.esp8266 import esp8266

class udpClient:

	def __init__(self, device, speed, timeout, debug=False):
		self.wifi = esp8266(device, speed, timeout, debug)
		self.debug = debug

	def connect(self, host, port):
		self.host = host
		self.port = port

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

		# Establish UDP transmission
		_command = "AT+CIPSTART=\"UDP\",\"{}\",{}".format(host, port)
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
