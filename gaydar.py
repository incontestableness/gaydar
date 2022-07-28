#!/usr/bin/env python3

__version__ = "0.1.0"

from flask import abort, Flask, jsonify, redirect, request, send_from_directory
from flask_caching import Cache
from flask_mqtt import Mqtt
import json
import netaddr



# Declare our Flask instance and define all the API routes
app = Flask(__name__)
config = {
	"JSON_SORT_KEYS": False,
	"CACHE_TYPE": "SimpleCache", # Flask-Caching
	"CACHE_DEFAULT_TIMEOUT": 5
}
app.config.from_mapping(config)
cache = Cache(app)
mqtt = Mqtt(app)


@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("MQTT client connected to broker!")
		mqtt.subscribe("zigbee2mqtt/bridge/state")
		mqtt.subscribe("zigbee2mqtt/bridge/event")
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


network_whitelists = [
	netaddr.IPNetwork("127.0.0.1/32"),
	netaddr.IPNetwork("192.168.1.0/24")
]

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


@app.route("/get_scenes")
def get_scenes():
	scenes = ["scene1", "scene2"]
	return jsonify(scenes=scenes)


@app.route("/set_color")
@app.route("/gaydar/set_color")
def set_color():
	color:str = request.args["color"]
	return "", 204


@app.route("/set_brightness")
@app.route("/gaydar/set_brightness")
def set_brightness():
	brightness = int(request.args["brightness"])
	payload = json.dumps({"brightness": brightness})
	mqtt.publish("zigbee2mqtt/bedroom/set", payload)
	return "", 204


@app.route("/toggle_lights")
@app.route("/gaydar/toggle_lights")
def toggle_lights():
	mqtt.publish("zigbee2mqtt/bedroom/set", json.dumps({"state": "TOGGLE"}))
	return "", 204


@app.route("/load_scene")
@app.route("/gaydar/load_scene")
def load_scene():
	name = request.args["scene_name"]
	return "", 204


@app.route("/save_scene")
@app.route("/gaydar/save_scene")
def save_scene():
	scene_name = request.args["scene_name"]
	color = request.args["color"]
	brightness = request.args["brightness"]
	return "", 204
