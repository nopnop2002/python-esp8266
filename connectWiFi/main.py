#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from esp8266.esp8266 import esp8266

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', help="uart device file name", default='/dev/tty')
	parser.add_argument('--speed', type=int, help="uart baudrate", default=115200)
	parser.add_argument('--timeout', type=int, help="uart timeout", default=3)
	parser.add_argument('--debug', action='store_true', help="enable debug print")
	args = parser.parse_args()
	print("device={}".format(args.device))
	print("speed={}".format(args.speed))
	print("debug={}".format(args.debug))

	wifi = esp8266(args.device, args.speed, args.timeout, args.debug)

	# Reset module
	ret = wifi.sendCommand("AT+RST", "WIFI GOT IP\r\n")
	if (ret is None): 
		print("AT+RST esp8266 not respond")
		sys.exit(1)

	# Local echo off
	ret = wifi.sendCommand("ATE0", "OK\r\n")
	if (ret is None): 
		print("ATE0 esp8266 not respond")
		sys.exit(2)

	ip = wifi.getIpInfo()
	print("ip={}".format(ip))

	mac = wifi.getMacInfo()
	print("mac={}".format(mac))
	sys.exit(0)
