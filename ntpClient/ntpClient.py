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
LOCAL_PORT = 12390		# Local port

class ntpClient:

	def __init__(self, device, speed, timeout, debug=False):
		self.wifi = esp8266(device, speed, timeout, debug)
		self.debug = debug

	def connect(self, host, timezone):
		self.host = host
		self.timezone = timezone

		_ret = self.wifi.sendCommand("AT+RST", "WIFI GOT IP\r\n")
		if (_ret is None):
			print("AT+RST esp8266 not respond")
			return None

		_ret = self.wifi.sendCommand("ATE0", "OK\r\n")
		if (_ret is None):
			print("ATE0 esp8266 not respond")
			return None

		_ret = self.wifi.setDNS(DNS_SERVER1, DNS_SERVER2)
		if (self.debug): print("_ret=[{}]".format(_ret))

		_command = "AT+CIPSTART=\"UDP\",\"0\",0,{},2".format(LOCAL_PORT)
		_ret = self.wifi.sendCommand(_command, "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if _ret is None:
			print("{} not respond".format(host))
			return False
		_ret = _ret.replace('\r\n', ' ')
		_ret = _ret.replace('OK', '')
		_ret = _ret.replace('"', '')
		_ret = _ret.rstrip()
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret != "CONNECT"):
			print("{} retuned {}".format(host, _ret[1]))
			return False

		return True

	def sendPacket(self):
		_packet = [0] * 48
		_packet[0] = 0b11100011;   # LI, Version, Mode
		_packet[1] = 0;			   # Stratum, or type of clock
		_packet[2] = 6;			   # Polling Interval
		_packet[3] = 0xEC;		   # Peer Clock Precision
		_packet[12] = 49;
		_packet[13] = 0x4E;
		_packet[14] = 49;
		_packet[15] = 52;
		__packet = str(_packet)
		if (self.debug): print("__packet={}".format(_packet))
		if (self.debug): print("len(__packet)={}".format(len(_packet)))
		if (self.debug): print("type(__packet)={}".format(type(_packet)))
		_ret = self.wifi.sendData(__packet, 48, self.host, 123)
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret == "OK"): return True
		return False

	def receivePacket(self):
		_ret = self.wifi.receiveData(False)
		if (self.debug): print("len(_ret)={}".format(len(_ret)))
		if (len(_ret) != 48): return None

		if (self.debug): print("_ret={}".format(_ret))
		if (self.debug): print("_ret[40]={}".format(_ret[40]))
		if (self.debug): print("_ret[41]={}".format(_ret[41]))
		if (self.debug): print("_ret[42]={}".format(_ret[42]))
		if (self.debug): print("_ret[43]={}".format(_ret[43]))
		_highWord = int.from_bytes(_ret[40], 'little')
		_highWord = _highWord * 256
		if (self.debug): print("_highWord=0x{:x}".format(_highWord))
		_highWord = _highWord + int.from_bytes(_ret[41], 'little')
		if (self.debug): print("_highWord=0x{:x}".format(_highWord))
		_lowWord = int.from_bytes(_ret[42], 'little')
		_lowWord = _lowWord * 256
		if (self.debug): print("_lowWord=0x{:x}".format(_lowWord))
		_lowWord = _lowWord + int.from_bytes(_ret[43], 'little')
		if (self.debug): print("_lowWord=0x{:x}".format(_lowWord))
		_secsSince1900 = _highWord << 16 | _lowWord
		if (self.debug): print("_secsSince1900={}".format(_secsSince1900))
		_seventyYears = 2208988800
		_epoch = _secsSince1900 - _seventyYears
		if (self.debug): print("_epoch={}".format(_epoch))
		_utc = datetime.datetime.utcfromtimestamp(_epoch)
		if (self.debug): print("_utc={}".format(_utc))
		_epoch = _epoch + (self.timezone * 60 * 60)
		_local = datetime.datetime.utcfromtimestamp(_epoch)
		if (self.debug): print("_local={}".format(_local))
		return _local
