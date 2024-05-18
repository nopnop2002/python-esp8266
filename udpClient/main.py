#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import os
import time
import argparse
from udpClient import udpClient

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', help="uart device file name", default='/dev/tty')
	parser.add_argument('--speed', type=int, help="uart baudrate", default=115200)
	parser.add_argument('--timeout', type=int, help="uart timeout", default=3)
	parser.add_argument('--host', help="udp host to connect to", default="255.255.255.255")
	parser.add_argument('--port', required=True, type=int, help="udp port to connect to")
	parser.add_argument('--debug', action='store_true', help="enable debug print")
	args = parser.parse_args()
	print("device={}".format(args.device))
	print("speed={}".format(args.speed))
	print("debug={}".format(args.debug))
	print("host={}".format(args.host))
	print("port={}".format(args.port))

	client = udpClient(args.device, args.speed, args.timeout, args.debug)

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
