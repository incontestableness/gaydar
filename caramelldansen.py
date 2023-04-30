#!/usr/bin/env python3

import argparse
import colorsys
import json
import paho.mqtt.client
import random
import sys
import time



parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-b", "--bpm", type=int, default=165)
parser.add_argument("-c", "--hue-change", type=int, default=45)
parser.add_argument("--hue-min", type=int, default=0)
parser.add_argument("--hue-max", type=int, default=360)
parser.add_argument("--base-topic", type=str, default="zigbee2mqtt")
parser.add_argument("-t", "--targets", type=str, default="fixture_1,fixture_2")
args = parser.parse_args()

# Sanity checks
if args.bpm > 300:
	print("Warning: Higher BPM values may begin to cause more noticeable desync between bulbs, or even intermittent color freezes.\n")

# Target parsing
args.targets = args.targets.split(",")


# Prepare to use the MQTT client
client = paho.mqtt.client.Client()
client.connect("localhost")

set_topics = []
for target in args.targets:
	set_topics.append(f"{args.base_topic}/{target}/set")
print(f"Set topics: {set_topics}")


# Calculate the update parameters
bps = args.bpm / 60
interval = (1000 / bps) / 1000
print(f"BPM: {args.bpm}")
print(f"BPS: {bps}")
print(f"Interval: {interval}")

# Used for displaying the current hue step
ERASE = "\x1b[2K"
CARRIAGE_RETURN = "\r"
count = 0
step_count = 360 / args.hue_change
print(f"Step count: {step_count}")

# Okay let's go
try:
	while True:
		for hue in range(args.hue_min, args.hue_max, args.hue_change):
			r, g, b = [int(color * 255) for color in colorsys.hls_to_rgb(hue / 360, 0.5, 1.0)]
			if args.verbose:
				print(f"Setting hue to {hue}")
			payload = {"color": {"r": r, "g": g, "b": b}}
			for st in set_topics:
				client.publish(st, json.dumps(payload))
			if count == step_count:
				if not args.verbose:
					sys.stdout.write(f"{ERASE}{CARRIAGE_RETURN}")
				count = 0
			if not args.verbose:
				sys.stdout.write(".")
			count += 1
			sys.stdout.flush()
			time.sleep(interval)
except BaseException as ex:
	sys.stdout.write("\n")
	if type(ex) != KeyboardInterrupt:
		raise
