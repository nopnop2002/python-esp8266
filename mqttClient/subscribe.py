#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import os
import time
import argparse
import signal
from mqttClient import mqttClient

def handler(signal, frame):
	global running
	print('handler')
	running = False

if __name__=="__main__":
	signal.signal(signal.SIGINT, handler)
	running = True

	parser = argparse.ArgumentParser()
	parser.add_argument('--device', required=True, help="uart device file name")
	parser.add_argument('--speed', type=int, help="uart baudrate", default=115200)
	parser.add_argument('--timeout', type=int, help="uart timeout", default=3)
	parser.add_argument('--host', help="mqtt host to connect to", default="broker.emqx.io")
	parser.add_argument('--port', type=int, help="mqtt port to connect to", default=1883)
	parser.add_argument('--topic', help="mqtt topic to subscribe to", default="/topic/esp8266")
	parser.add_argument('--qos', type=int, choices=range(0, 3), help="mqtt qos to publish to", default=0)
	parser.add_argument('--forever', action='store_true', help="enable forever loop")
	parser.add_argument('--debug', action='store_true', help="enable debug print")
	args = parser.parse_args()
	print("device={}".format(args.device))
	print("speed={}".format(args.speed))
	print("debug={}".format(args.debug))
	print("host={}".format(args.host))
	print("port={}".format(args.port))
	print("topic={}".format(args.topic))
	print("qos={}".format(args.qos))
	print("forever={}".format(args.forever))

	if (args.forever): print("Press Ctrl+c to stop")

	client = mqttClient(args.device, args.speed, args.timeout, args.debug)

	# Connect server
	ret = client.connect(args.host, args.port, args.qos)
	print("client.connect = {}".format(ret))
	if (ret is False):
		sys.exit(1)

	# Subscribe topic
	ret = client.subscribe(args.topic)
	print("client.subscribe = {}".format(ret))
	if (ret is False):
		sys.exit(2)

	while running:
		# Receive topics
		ret = client.update()
		#print("client.update = {} {}".format(ret, type(ret)))
		if (ret is False):
			sys.exit(3)

		# Retrieve received topics
		received = client.subscribed()
		#print("client.subscribed = {}".format(received))
		if (received is not None):
			#print(len(received))
			for receive in received:
				print("topic=[{}] payload=[{}]".format(receive[0], receive[1]))
			if (args.forever is False): break
		time.sleep(1)

	# Disconnect server
	ret = client.disconnect()
	print("client.disconnect = {}".format(ret))
	sys.exit(0)
