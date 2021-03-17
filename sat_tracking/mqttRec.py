#mqttRec.py
#!/usr/bin/python3
import paho.mqtt.client as mqtt

def message_receive_callback(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_message = message_receive_callback

mqtt_username = "xrosxprm"
mqtt_password = "i5LvdfdUqJY-"
client.username_pw_set(mqtt_username, mqtt_password)
mqtt_host = "tailor.cloudmqtt.com"
mqtt_port = 10720
client.connect(mqtt_host, mqtt_port, keepalive=60)
client.subscribe("test")
client.loop_forever()
