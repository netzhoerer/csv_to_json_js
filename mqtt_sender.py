#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.publish as publish

MQTT_SERVER = "10.0.1.23"
MQTT_PATH = "test_channel"

publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)
