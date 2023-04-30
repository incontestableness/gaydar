#!/usr/bin/env python3

__version__ = "0.1.0"

from flask import abort, Flask, jsonify, redirect, request, send_from_directory
from flask_caching import Cache
from flask_mqtt import Mqtt
import json
import netaddr
import yaml



# === Declare our Flask instance ===


app = Flask(__name__)
config = {
	"JSON_SORT_KEYS": False,
	"CACHE_TYPE": "SimpleCache", # Flask-Caching
	"CACHE_DEFAULT_TIMEOUT": 5
}
app.config.from_mapping(config)
cache = Cache(app)
mqtt = Mqtt(app)

# We respond to most API requests with 204 No Content
no_content = ("", 204)


# === Configuration ===


# Target all devices configured in data/devices.yaml by default
app.targets = ["all"]

# The set topics to send payloads to
app.set_targets = []

# Network spaces that are allowed to control the lights
network_whitelists = [
	netaddr.IPNetwork("127.0.0.0/8"),
	netaddr.IPNetwork("192.168.0.0/16"),
	netaddr.IPNetwork("10.0.0.0/8")
]

# Load groups/devices to target
@app.before_first_request
def reload_configuration():
	app.set_targets = []
	with open("/opt/zigbee2mqtt/data/groups.yaml") as f:
		groups = yaml.safe_load(f)
	with open("/opt/zigbee2mqtt/data/devices.yaml") as f:
		devices = yaml.safe_load(f)
	for group_number in groups:
		group = groups[group_number]
		# If the user configured a group with this name, ignore it
		if group["friendly_name"] == "all":
			break
		if group["friendly_name"] in app.targets:
			for target in group["devices"]:
				app.set_targets.append(f"zigbee2mqtt/{target}/set")
	for device_number in devices:
		device = devices[device_number]
		if app.targets == ["all"]:
			app.set_targets.append(f"zigbee2mqtt/{device['friendly_name']}/set")
		elif device["friendly_name"] in app.targets:
			app.set_targets.append(f"zigbee2mqtt/{device['friendly_name']}/set")
	print(f"Set targets: {app.set_targets}")


# === MQTT ===


@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("MQTT client connected to broker!")
		mqtt.subscribe("zigbee2mqtt/bridge/state")
		print("Subscribed!")
	else:
		print(f"Bad connection. Code: {rc}")


@mqtt.on_disconnect()
def on_disconnect():
	print("MQTT client disconnected from broker...")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	payload = message.payload.decode()
	print(f"Received message on topic {message.topic}: {payload}")


# Send the given payload to each target device
def send(payload):
	for set_target in app.set_targets:
		mqtt.publish(set_target, payload)


# === Flask routes ===


@app.before_request
def ensure_whitelisted():
	requester_ip = netaddr.IPAddress(request.remote_addr, version=4)
	for network in network_whitelists:
		if requester_ip in network:
			return
	abort(403)


# Redirect to static content
@app.route("/")
@cache.cached(timeout=60 * 60)
def root():
	return redirect(location="/gaydar.html")


# When run directly, we're expected to serve this file
@app.route("/gaydar.html")
def gaydar():
	return send_from_directory("html", "gaydar.html")


@app.route("/set_color")
@app.route("/gaydar/set_color")
def set_color():
	color:str = request.args["color"]
	send(json.dumps({"color": {"hex": color}}))
	return no_content


# really need color temp slider on gaydar...
# I don't want to use the sengled's inverse mired scale thing
@app.route("/set_color_temperature")
@app.route("/gaydar/set_color_temperature")
def set_color_temperature():
	color_temperature:str = request.args["color_temperature"]
	send(json.dumps({"color_temp": color_temperature}))
	return no_content


@app.route("/set_brightness")
@app.route("/gaydar/set_brightness")
def set_brightness():
	brightness = int(request.args["brightness"])
	payload = json.dumps({"brightness": brightness})
	send(payload)
	return no_content


@app.route("/toggle_lights")
@app.route("/gaydar/toggle_lights")
def toggle_lights():
	send(json.dumps({"state": "TOGGLE"}))
	return no_content


# === Zigbee2MQTT scene routes ===


@app.route("/get_scenes")
@app.route("/gaydar/get_scenes")
def get_scenes():
	scenes = ["scene1", "scene2"]
	return jsonify(scenes=scenes)


@app.route("/load_scene")
@app.route("/gaydar/load_scene")
def load_scene():
	name = request.args["scene_name"]
	return no_content


@app.route("/save_scene")
@app.route("/gaydar/save_scene")
def save_scene():
	scene_name = request.args["scene_name"]
	color = request.args["color"]
	brightness = request.args["brightness"]
	return no_content


# === Target device control ===


@app.route("/set_target_names")
@app.route("/gaydar/set_target_names")
def set_target_names():
	app.targets = request.args["targets"].split(",")
	reload_configuration()
	return no_content
