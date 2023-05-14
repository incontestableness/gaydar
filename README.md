# this is actually just a (quite possibly outdated) todo list


## here's some quick documentation though:

you'll need:
* zigbee2mqtt
* mosquitto (or some other mqtt server for zigbee2mqtt)
	* todo: add sample mosquitto config to repo for ideal performance
	https://mosquitto.org/man/mosquitto-conf-5.html

## you might want some other stuff like homebridge-z2m
* homebridge-z2m requires [Homebridge](https://github.com/homebridge/homebridge/wiki/Install-Homebridge-on-Raspbian#installing-homebridge) to be installed first
	* be sure to access the web interface and make an account, apt will give you a nice message
	* homebridge-z2m provides a systemd service named `hb-service`
* homebridge-z2m install: https://z2m.dev/install.html
	* I recommend just using the homebridge-z2m web UI to search "z2m" under the plugins tab and install from there
	* if you only bind mosquitto to IPv4 you will need to change localhost to 127.0.0.1 because nodejs is retarded


## general info/resources
* https://www.zigbee2mqtt.io/devices/E21-N1EA.html
* https://www.zigbee2mqtt.io/guide/usage/scenes.html#creating-a-scene


## feature todo
* inverse mired scale conversion?
* color temperature slider

* caramelldansen integration into flask, see below for ideas?
* scheduled lights with sunrise/sunset via multiprocessing lock (for stopping sun colors) and value (for delaying resumption of sun colors)


## Problems and links

### daylight cycle, mired scale, color temperature (K)
* https://en.wikipedia.org/wiki/Azimuth?useskin=vector
* https://en.wikipedia.org/wiki/Mired?useskin=vector
* https://en.wikipedia.org/wiki/Color_temperature?useskin=vector

### the HTTP 204 problem on iOS: maybe just redirect back to the same page?
* https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
* https://stackoverflow.com/questions/41270855/flask-redirect-to-same-page-after-form-submission

### not sure what this was for
* https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request

### restructuring to accomodate other features? namely I expect we wanted to do something relying on async
* https://flask.palletsprojects.com/en/2.2.x/async-await/
* https://github.com/pallets/quart
* https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files
* https://flask.palletsprojects.com/en/2.2.x/patterns/packages/

### get playing spotify track BPM
* https://developer.spotify.com/documentation/web-api/reference/get-information-about-the-users-current-playback
* https://developer.spotify.com/documentation/web-api/reference/get-audio-features
* https://stackoverflow.com/questions/42667973/api-provide-track-bpm-tempo
* https://developer.spotify.com/documentation/web-api/concepts/authorization
* https://tekore.readthedocs.io/en/stable/index.html
* https://tekore.readthedocs.io/en/stable/reference/models.html#tekore.model.FullTrack

### midi-based light colors
* https://freemidi.org/
* https://mido.readthedocs.io/en/latest/
