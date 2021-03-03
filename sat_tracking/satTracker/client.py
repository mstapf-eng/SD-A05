##client.py
#!/usr/bin/python3

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

passUser = {"username": "xrosxprm", "password": "i5LvdfdUqJY-"}
topic = "test"
def sendMessage(message):
    publish.single(topic, payload=message, qos=0, retain=False, hostname="tailor.cloudmqtt.com",
                   port=10720, client_id="", keepalive=60, will=None, auth=passUser, tls=None,
                   protocol=mqtt.MQTTv311, transport="tcp")



sendMessage("This is a test")
