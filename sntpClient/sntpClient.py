#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from esp8266.esp8266 import esp8266

DNS_SERVER1 = "8.8.8.8" # DNS SERVER1
DNS_SERVER2 = "8.8.4.4" # DNS SERVER2

class sntpClient:

	def __init__(self, device, speed, timeout, debug=False):
		self.wifi = esp8266(device, speed, timeout, debug)
		self.debug = debug

	def connect(self, host, timezone):
		self.host = host
		self.timezone = timezone

		# Reset module
		_ret = self.wifi.sendCommand("AT+RST", "WIFI GOT IP\r\n")
		if (_ret is None):
			print("AT+RST esp8266 not respond")
			return None

		# Local echo off
		_ret = self.wifi.sendCommand("ATE0", "OK\r\n")
		if (_ret is None):
			print("ATE0 esp8266 not respond")
			return None

		# Set DNS Server Information
		_ret = self.wifi.setDNS(DNS_SERVER1, DNS_SERVER2)
		if (self.debug): print("_ret=[{}]".format(_ret))

		# Set the time zone and SNTP server
		_command = 'AT+CIPSNTPCFG=1,{},\"{}\"'.format(timezone, host)
		if (self.debug): print("_command=[{}]".format(_command))
		_ret = self.wifi.sendCommand(_command, "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if _ret is None:
			print("{} not respond".format(host))
			return False
		_ret = _ret.replace('\r\n', '')
		_ret = _ret.replace(' ', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret != "OK"): return False
		
		return True

	def getTime(self):
		for _i in range(3):
			_ret = self.wifi.sendCommand("AT+CIPSNTPTIME?", "OK\r\n")
			if (self.debug): print("_ret=[{}]".format(_ret))
			_ret = _ret.replace('\r\n', ' ')
			_ret = _ret.replace('OK', '')
			if (self.debug): print("_ret=[{}]".format(_ret))
			_ret = _ret.rstrip()
			if (self.debug): print("_ret=[{}]".format(_ret))

			_index = _ret.find(':')
			if (self.debug): print("_index=[{}]".format(_index))
			if (_index == -1): break
			_time = _ret[_index+1:]
			if (self.debug): print("_time=[{}]".format(_time))
			if (_time != 'Thu Jan 01 00:00:00 1970'): return _time
			time.sleep(1)

		return None
