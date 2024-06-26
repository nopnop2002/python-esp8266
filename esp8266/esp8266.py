#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import serial

class esp8266:

	def __init__(self, device, speed, timeout, debug=False):
		# Open serial port
		self.debug = debug
		#self.ser = serial.Serial(device, speed, timeout=1.0)
		self.ser = serial.Serial(device, speed, timeout=timeout)

	def sendCommand(self, command, wait):
		"""
		Send AT command and wait responce
		"""
		if (self.debug): print("command=[{}]".format(command))
		_command = command + "\r\n"
		self.ser.flushInput()
		#print("{}".format(str.encode(_command)))
		self.ser.write(str.encode(_command))

		_wait = list(wait)
		_waitlen = len(_wait) * -1
		#if (self.debug): print("_wait={}".format(_wait))
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("sendCommand: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))
			_last = _received[_waitlen:]
			if (self.debug): print("_wait={}".format(_wait))
			if (self.debug): print("_last={}".format(_last))
			if (_wait == _last): break

		self.ser.flushInput()
		_return = "".join(_received)
		#if (self.debug): print("_return={}".format(_return))
		return _return

	def sendData(self, data, size, host, port, binary=False):
		"""
		Send data to host and port
		"""
		if (host is not None):
			_command = "AT+CIPSEND={},\"{}\",{}".format(size, host, port)
		else:
			_command = "AT+CIPSEND={}".format(size)
		if (self.debug): print("_command=[{}]".format(_command))
		_command = _command + "\r\n"
		self.ser.flushInput()
		#wk = str.encode(_command)
		#print(type(wk))
		self.ser.write(str.encode(_command))

		_wait = list("OK\r\n")
		_waitlen = len(_wait) * -1
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("sendCommand: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))
			_last = _received[_waitlen:]
			if (self.debug): print("_wait={}".format(_wait))
			if (self.debug): print("_last={}".format(_last))
			if (_wait == _last): break

		_wait = list("> ")
		_waitlen = len(_wait) * -1
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("sendCommand: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))
			_last = _received[_waitlen:]
			if (self.debug): print("_wait={}".format(_wait))
			if (self.debug): print("_last={}".format(_last))
			if (_wait == _last): break
			#if (ch == ">"): break

		for _i in range(size):
			if (binary):
				if (self.debug): print("{}={}".format(_i, data[_i].to_bytes(1, 'little')))
				self.ser.write(data[_i].to_bytes(1, 'little'))
			else:
				if (self.debug): print("{}={}".format(_i, str.encode(data[_i])))
				self.ser.write(str.encode(data[_i]))

		_wait = list("SEND OK\r\n")
		_waitlen = len(_wait) * -1
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("sendCommand: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))
			_last = _received[_waitlen:]
			if (self.debug): print("_wait={}".format(_wait))
			if (self.debug): print("_last={}".format(_last))
			if (_wait == _last): break

		return "OK"

	def receiveData(self, binary=False):
		"""
		Receiving undefined length data
		+IPD,{size}:{data}
		+IPD,10:1234567890
		"""
		_wait = list("+IPD,")
		_waitlen = len(_wait) * -1
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("receiveData: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))
			_last = _received[_waitlen:]
			if (self.debug): print("_wait={}".format(_wait))
			if (self.debug): print("_last={}".format(_last))
			if (_wait == _last): break
			
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("receiveData: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			if (ch == ":"): break
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))

		_size = "".join(_received)
		if (self.debug): print("_size=[{}]".format(_size))
		_size = int(_size)
		if (self.debug): print("_size={}".format(_size))

		_received = []
		for _i in range(_size):
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("receiveData: timeout")
				return None
			if (binary is False):
				ch = ch.decode('utf-8')
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))

		if (binary):
			_return = _received
		else:
			_return = "".join(_received)
		if (self.debug): print("_return={}".format(_return))
		return _return

	def waitData(self, wait, binary=False):
		"""
		Receiving fixed length data
		+IPD,{size_of_wait}:{wait}
		+IPD,10:1234567890
		"""
		_wait = list(wait)
		_waitlen = len(_wait) * -1
		if (self.debug): print("_wait={}".format(_wait))
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				print("waitData: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))
			_last = _received[_waitlen:]
			if (self.debug): print("_wait={}".format(_wait))
			if (self.debug): print("_last={}".format(_last))
			if (_wait == _last): break

		self.ser.flushInput()
		if (binary):
			_return = _received
		else:
			_return = "".join(_received)
		#if (self.debug): print("_return={}".format(_return))
		return _return

	def isWaiting(self):
		"""
		Returns the size of the data arrived at the objects internal buffer
		"""
		return self.ser.in_waiting

	def readData(self, length, binary=False):
		"""
		Receive data for length
		"""
		_received = []
		while True:
			ch = self.ser.read()
			if (self.debug): print("ch={} {}".format(len(ch), ch))
			if (len(ch) == 0): 
				return []
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))
			if (len(_received) == length): break

		if (binary):
			_return = _received
		else:
			_return = "".join(_received)
		return _return

	def getApInfo(self):
		_ret = self.sendCommand("AT+CWJAP?", "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret is None): return _ret

		_ret = _ret.replace('\r\n', ' ')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('"', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('OK', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace(' ', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		if (_ret[0:4] == "NoAP"): return None
		_ret = _ret.split(':')
		if (self.debug): print("_ret=[{}]".format(_ret))
		return _ret[1]

	def getIpInfo(self):
		_ret = self.sendCommand("AT+CIPSTA?", "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('\r\n', ' ')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('"', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.split(' ')

		_ip = _ret[1]
		if (self.debug): print("_ip=[{}]".format(_ip))
		_ip = _ip.split(':')
		_ip = _ip[2]
		if (self.debug): print("_ip=[{}]".format(_ip))

		_gateway = _ret[2]
		if (self.debug): print("_gateway=[{}]".format(_gateway))
		_gateway = _gateway.split(':')
		_gateway = _gateway[2]
		if (self.debug): print("_gateway=[{}]".format(_gateway))

		_netmask = _ret[2]
		if (self.debug): print("_netmask=[{}]".format(_netmask))
		_netmask = _netmask.split(':')
		_netmask = _netmask[2]
		if (self.debug): print("_netmask=[{}]".format(_netmask))
		return [_ip, _gateway, _netmask]

	def getMacInfo(self):
		_ret = self.sendCommand("AT+CIFSR", "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('\r\n', '')
		_ret = _ret.replace('OK', '')
		_ret = _ret.replace('"', '')
		_ret = _ret.replace(' ', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.split(',')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_mac = _ret[2]
		return _mac

	def setDNS(self, dns1, dns2=None, dns3=None):
		if (dns3 is not None):
			_command = 'AT+CIPDNS_CUR=1,\"{}\",\"{}\",\"{}\"'.format(dns1,dns2,dns3)
		elif (dns2 is not None):
			_command = 'AT+CIPDNS_CUR=1,\"{}\",\"{}\"'.format(dns1,dns2)
		else:
			_command = 'AT+CIPDNS_CUR=1,\"{}\"'.format(dns1)
		if (self.debug): print("_command=[{}]".format(_command))
		_ret = self.sendCommand(_command, "OK\r\n")
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('\r\n', ' ')
		_ret = _ret.replace('OK', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('"', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace(' ', '')
		if (self.debug): print("_ret=[{}]".format(_ret))

		_dns = _ret.split(',')
		if (self.debug): print("_dns=[{}]".format(_dns))
		if (len(_dns) == 2): return _dns[1]
		if (len(_dns) == 3): return [_dns[1], _dns[2]]
		if (len(_dns) == 4): return [_dns[1], _dns[2], _dns[3]]
		return None
