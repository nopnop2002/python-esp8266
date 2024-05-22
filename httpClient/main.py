#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import os
import time
import argparse
from httpClient import httpClient

PATH = "/sample"

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', help="uart device file name", default='/dev/tty')
	parser.add_argument('--speed', type=int, help="uart baudrate", default=115200)
	parser.add_argument('--timeout', type=int, help="uart timeout", default=3)
	parser.add_argument('--host', required=True, help="http host to connect to")
	parser.add_argument('--port', required=True, type=int, help="http port to connect to")
	parser.add_argument('--debug', action='store_true', help="enable debug print")
	args = parser.parse_args()
	print("device={}".format(args.device))
	print("speed={}".format(args.speed))
	print("debug={}".format(args.debug))
	print("host={}".format(args.host))
	print("port={}".format(args.port))

	client = httpClient(args.device, args.speed, args.timeout, args.debug)

	# Start WiFi
	ret = client.start(args.host, args.port)
	print("client.start = {}".format(ret))
	if (ret is False):
		sys.exit(1)

	# Request GET
	ret = client.get(PATH)
	print("client.get = {}".format(ret))
	if (ret == False):
		header = client.responceHeader()
		print("http error {}".format(header))
		sys.exit(2)
	body = client.responceBody()
	print("{}".format(body))
	print("Hit Enter key to Put new record")
	sys.stdin.read(1)

	# Request POST
	ret = client.post(PATH, "{\"title\":\"test\",\"auther\":\"nopnop2002\"}")
	print("client.post = {}".format(ret))
	if (ret == False):
		header = client.responceHeader()
		print("http error {}".format(header))
		sys.exit(3)
	#body = client.responceBody()
	#print("{}".format(body))

	# Request GET
	ret = client.get(PATH)
	print("client.get = {}".format(ret))
	if (ret == False):
		header = client.responceHeader()
		print("http error {}".format(header))
		sys.exit(4)
	body = client.responceBody()
	print("{}".format(body))
	print("Hit Enter key to modify record")
	sys.stdin.read(1)

	# Request PUT
	path = "{}/2".format(PATH)
	ret = client.put(path, "{\"title\":\"test_update\",\"auther\":\"nopnop2002_update\"}")
	print("client.put = {}".format(ret))
	if (ret is False):
		header = client.responceHeader()
		print("http error {}".format(header))
		sys.exit(5)
	body = client.responceBody()
	print("{}".format(body))
	print("Hit Enter key to delete record")
	sys.stdin.read(1)

	# Request DELETE
	path = "{}/2".format(PATH)
	ret = client.delete(path)
	print("client.delete = {}".format(ret))
	if (ret is False):
		header = client.responceHeader()
		print("http error {}".format(header))
		sys.exit(6)

	# Request GET
	ret = client.get(PATH)
	print("client.get = {}".format(ret))
	if (ret == False):
		header = client.responceHeader()
		print("http error {}".format(header))
		sys.exit(7)
	body = client.responceBody()
	print("{}".format(body))

