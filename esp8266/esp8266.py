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

	def sendData(self, data, size, host, port):
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
			if (ch == ">"): break

		for _i in range(size):
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

	def receiveData(self):
		_wait = list("IPD,")
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
				print("sendCommand: timeout")
				return None
			try:
				ch = ch.decode('utf-8')
			except:
				continue
			_received.append(ch)
			if (self.debug): print("_recieved={}".format(_received))

		_return = "".join(_received)
		if (self.debug): print("_return={}".format(_return))
		return _return

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
		_ret = _ret.replace('\r\n', ' ')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.replace('"', '')
		if (self.debug): print("_ret=[{}]".format(_ret))
		_ret = _ret.split(' ')

		_mac = _ret[2]
		if (self.debug): print("_mac=[{}]".format(_mac))
		_mac = _mac.split(',')
		_mac = _mac[1]
		if (self.debug): print("_mac=[{}]".format(_mac))
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
