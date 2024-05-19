#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import os
import argparse
from sntpClient import sntpClient

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', help="uart device file name", default='/dev/tty')
	parser.add_argument('--speed', type=int, help="uart baudrate", default=115200)
	parser.add_argument('--timeout', type=int, help="uart timeout", default=3)
	parser.add_argument('--host', help="time server", default="time.google.com")
	parser.add_argument('--timezone', type=int, help="timezone", default=0)
	parser.add_argument('--debug', action='store_true', help="enable debug print")
	args = parser.parse_args()
	print("device={}".format(args.device))
	print("speed={}".format(args.speed))
	print("debug={}".format(args.debug))
	print("host={}".format(args.host))
	print("timezone={}".format(args.timezone))

	client = sntpClient(args.device, args.speed, args.timeout, args.debug)

	# Connect server
	ret = client.connect(args.host, args.timezone)
	print("client.connect = {}".format(ret))
	if (ret is False):
		sys.exit(1)

	# Get time from server
	datetime = client.getTime()
	print("datetime is [{}]".format(datetime))
	sys.exit(0)

