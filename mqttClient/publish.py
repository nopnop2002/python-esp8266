#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import os
import time
import argparse
from mqttClient import mqttClient

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', required=True, help="uart device file name")
	parser.add_argument('--speed', type=int, help="uart baudrate", default=115200)
	parser.add_argument('--timeout', type=int, help="uart timeout", default=3)
	parser.add_argument('--host', help="mqtt host to connect to", default="broker.emqx.io")
	parser.add_argument('--port', type=int, help="mqtt port to connect to", default=1883)
	parser.add_argument('--topic', help="mqtt topic to publish to", default="/topic/esp8266")
	parser.add_argument('--payload', help="mqtt payload to publish to", default="test")
	parser.add_argument('--qos', type=int, choices=range(0, 3), help="mqtt qos to publish to", default=0)
	parser.add_argument('--debug', action='store_true', help="enable debug print")
	args = parser.parse_args()
	print("device={}".format(args.device))
	print("speed={}".format(args.speed))
	print("debug={}".format(args.debug))
	print("host={}".format(args.host))
	print("port={}".format(args.port))
	print("topic={}".format(args.topic))
	print("payload={}".format(args.payload))
	print("qos={}".format(args.qos))

	client = mqttClient(args.device, args.speed, args.timeout, args.debug)

	# Connect server
	ret = client.connect(args.host, args.port, args.qos)
	print("client.connect = {}".format(ret))
	if (ret is False):
		sys.exit(1)

	# Publish topic
	ret = client.publish(args.topic, args.payload)
	print("client.publish = {}".format(ret))
	if (ret is False):
		sys.exit(2)

	# Disconnect server
	ret = client.disconnect()
	print("client.disconnect = {}".format(ret))
	sys.exit(0)
