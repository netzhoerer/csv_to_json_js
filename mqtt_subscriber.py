#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import simpleaudio as sa

# def on_message(client, userdata, message):
#     msg = str(message.payload.decode("utf-8"))
#     print("message received: ", msg)
#     print("message topic: ", message.topic)


# def on_connect(client, userdata, flags, rc):
#     client.subscribe('/home/data')


# BROKER_ADDRESS = "10.0.1.12"

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(BROKER_ADDRESS)

# print("Connected to MQTT Broker: " + BROKER_ADDRESS)

# client.loop_forever()

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"
global play_obj

wave_obj = sa.WaveObject.from_wave_file(
    '/home/pi/projects/mqtt-responder/a2002011001-e02.wav')


# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # play_obj = wave_obj.play()
    # play_obj.wait_done()

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.


# publish.single is the same as  mosquitto_pub -h 10.0.1.23 -t test_channel -m "Ich habe Hunger"
def on_message(client, userdata, msg):
    msg_payload = msg.payload.decode('utf-8')
    print(msg.topic+" "+str(msg_payload))
    if str(msg_payload) == "torsten":
        publish.single(msg.topic + "/answer",
                       "yep that's right", hostname=MQTT_SERVER, qos=2, retain=False)
    elif str(msg_payload) == "music":
        play_obj = wave_obj.play()
        publish.single(msg.topic + "/answer",
                       "music started", hostname=MQTT_SERVER, qos=2, retain=False)
        # play_obj.wait_done()
    elif str(msg_payload) == "stop":
        sa.stop_all()
        publish.single(msg.topic + "/answer",
                       "music finished", hostname=MQTT_SERVER, qos=2, retain=False)
    else:
        publish.single(msg.topic + "/answer",
                       "nope thats wrong", hostname=MQTT_SERVER, qos=2, retain=False)
# more callbacks, etc


def on_disconnect(client, userdata, rc=0):
    print("DisConnected result code "+str(rc))
    client.loop_stop()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
