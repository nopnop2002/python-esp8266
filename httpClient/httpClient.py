#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from esp8266.esp8266 import esp8266

class httpClient:

	def __init__(self, device, speed, timeout, debug=False):
		self.wifi = esp8266(device, speed, timeout, debug)
		self.debug = debug

	def start(self, host, port):
		self.host = host
		self.port = port

		# Get AP info
		_ret = self.wifi.getApInfo()

		# Reset module
		if (_ret is None):
			_ret = self.wifi.sendCommand("AT+RST", "WIFI GOT IP\r\n")
			if (_ret is None):
				print("AT+RST esp8266 not respond")
				return None

		# Local echo off
		_ret = self.wifi.sendCommand("ATE0", "OK\r\n")
		if (_ret is None):
			print("ATE0 esp8266 not respond")
			return None

		return True

	def connectServer(self):
		# Establish TCP transmission
		_command = "AT+CIPSTART=\"TCP\",\"{}\",{}".format(self.host, self.port)
		_ret = self.wifi.sendCommand(_command, "OK\r\n")
		if (self.debug): print("sendCommand _ret=[{}]".format(_ret))
		if _ret is None:
			print("{} not respond".format(self.host))
			return False

		_ret = _ret.replace('\r\n', '')
		_ret = _ret.replace('OK', '')
		_ret = _ret.replace(' ', '')
		if (self.debug): print("AT+CIPSTART _ret=[{}]".format(_ret))
		if (_ret != "CONNECT"): return False
		return True

	def closeServer(self):
		# Close TCP connection
		_ret = self.wifi.sendCommand("AT+CIPCLOSE", "OK\r\n")
		if (self.debug): print("sendCommand _ret=[{}]".format(_ret))
		if (_ret is None): return False

		_ret = _ret.replace('\r\n', '')
		_ret = _ret.replace('OK', '')
		_ret = _ret.replace(' ', '')
		if (self.debug): print("AT+CIPCLOSE _ret=[{}]".format(_ret))
		if (_ret != "CLOSED"): return False
		return True

	def requestHeader(self, request, path):
		_header = "{} /{} HTTP/1.1\r\nHost: {}:{}\r\nUser-Agent: esp8266/1.0.0\r\nAccept: */*\r\n".format(request, path, self.host, self.port)
		return _header

	def responseHeader(self):
		return self.header

	def responseBody(self):
		return self.body

	def get(self, path):
		self.header = None
		self.body = None

		# Establish TCP transmission
		_ret = self.connectServer()
		if (self.debug): print("connectServer _ret={}".format(_ret))
		if (_ret is False): return False

		# Send packet
		_path = path
		if (path[0] == "/"):
			_path = path[1:]
		_data = self.requestHeader("GET", _path)
		_data = _data + "\r\n"
		_ret = self.wifi.sendData(_data, len(_data), None, 0)
		if (self.debug): print("sendData _ret=[{}]".format(_ret))
		if (_ret is False): return False

		# Receive packet
		_ret = self.receivePacket()
		if (self.debug): print("receivePacket _ret={}".format(_ret))
		self.header = _ret[1]
		self.body = _ret[2]
		if (_ret[0] is False): return False
		
		# Close TCP connection
		_ret = self.closeServer()
		if (self.debug): print("closeServer _ret={}".format(_ret))
		if (_ret is False): return False
		
		return True

	def post(self, path, json):
		self.header = None
		self.body = None

		# Establish TCP transmission
		_ret = self.connectServer()
		if (self.debug): print("connectServer _ret={}".format(_ret))
		if (_ret is False): return False

		# Send packet
		_path = path
		if (path[0] == "/"):
			_path = path[1:]
		_data = self.requestHeader("POST", _path)
		_data = _data + "Content-Type: application/json\r\n"
		_data = _data + "Content-Length: {}\r\n".format(len(json))
		_data = _data + "\r\n"
		_data = _data + json
		_ret = self.wifi.sendData(_data, len(_data), None, 0)
		if (self.debug): print("sendData _ret=[{}]".format(_ret))
		if (_ret is False): return False

		# Receive packet
		_ret = self.receivePacket()
		if (self.debug): print("receivePacket _ret={}".format(_ret))
		self.header = _ret[1]
		if (_ret[0] is False): return False

		# Close TCP connection
		_ret = self.closeServer()
		if (self.debug): print("closeServer _ret={}".format(_ret))
		if (_ret is False): return False

		return True

	def put(self, path, json):
		self.header = None
		self.body = None

		# Establish TCP transmission
		_ret = self.connectServer()
		if (self.debug): print("connectServer _ret={}".format(_ret))
		if (_ret is False): return False

		# Send packet
		_path = path
		if (path[0] == "/"):
			_path = path[1:]
		_data = self.requestHeader("PUT", _path)
		_data = _data + "Content-Type: application/json\r\n"
		_data = _data + "Content-Length: {}\r\n".format(len(json))
		_data = _data + "\r\n"
		_data = _data + json
		_ret = self.wifi.sendData(_data, len(_data), None, 0)
		if (self.debug): print("sendData _ret=[{}]".format(_ret))
		if (_ret is False): return False

		# Receive packet
		_ret = self.receivePacket()
		if (self.debug): print("receivePacket _ret={}".format(_ret))
		self.header = _ret[1]
		self.body = _ret[2]
		if (_ret[0] is False): return False

		# Close TCP connection
		_ret = self.closeServer()
		if (self.debug): print("closeServer _ret={}".format(_ret))
		if (_ret is False): return False

		return True

	def delete(self, path):
		self.header = None
		self.body = None

		# Establish TCP transmission
		_ret = self.connectServer()
		if (self.debug): print("connectServer _ret={}".format(_ret))
		if (_ret is False): return False

		# Send packet
		_path = path
		if (path[0] == "/"):
			_path = path[1:]
		_data = self.requestHeader("DELETE", _path)
		_data = _data + "\r\n"
		_ret = self.wifi.sendData(_data, len(_data), None, 0)
		if (self.debug): print("sendData _ret=[{}]".format(_ret))

		# Receive packet
		_ret = self.receivePacket()
		if (self.debug): print("receivePacket _ret={}".format(_ret))
		self.header = _ret[1]
		self.body = _ret[2]
		if (_ret[0] is False): return False

		# Close TCP connection
		_ret = self.closeServer()
		if (self.debug): print("closeServer _ret={}".format(_ret))
		if (_ret is False): return False

		return True

	def receivePacket(self):
		_ret = self.wifi.receiveData()
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is None): return [False, None, None]

		_find = _ret.find("\r\n\r\n")
		if (self.debug): print("_find={}".format(_find))
		_header = _ret[0:_find]
		_body = _ret[_find+4:]
		_headers = _header.splitlines()
		if (self.debug): print("_headers={}".format(_headers))
		if (_headers[0] == "HTTP/1.1 200 OK"):
			return [True, _header, _body]
		elif (_headers[0] == "HTTP/1.1 201 Created"):
			return [True, _header, None]
		else:
			return [False, _header, None]

