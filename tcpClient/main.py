#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import os
import time
import argparse
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#from esp8266.esp8266 import esp8266
from tcpClient import tcpClient

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', help="uart device file name", default='/dev/tty')
	parser.add_argument('--speed', type=int, help="uart baudrate", default=115200)
	parser.add_argument('--timeout', type=int, help="uart timeout", default=3)
	parser.add_argument('--host', required=True, help="tcp host to connect to")
	parser.add_argument('--port', required=True, type=int, help="tcp port to connect to")
	parser.add_argument('--debug', action='store_true', help="enable debug print")
	args = parser.parse_args()
	print("device={}".format(args.device))
	print("speed={}".format(args.speed))
	print("debug={}".format(args.debug))
	print("host={}".format(args.host))
	print("port={}".format(args.port))

	client = tcpClient(args.device, args.speed, args.timeout, args.debug)

	# Connect server
	ret = client.connect(args.host, args.port)
	print("client.connect = {}".format(ret))
	if (ret is False):
		sys.exit()

	for loop in range(10):
		# Send data to server
		data = "Hello! World! {}".format(loop)
		ret = client.send(data, len(data))
		print("client.send = {}".format(ret))
		if (ret is False):
			sys.exit()

		# Recive data from server
		ret = client.receive()
		print("client.receive = {}".format(ret))
		time.sleep(1)


	# Disconnect server
	ret = client.disconnect()
	print("client.disconnect = {}".format(ret))
