# Creating MQTT Client and Connecting to MQTT Broker
## Set up the cloud broker
For this project, I used cloudMQTT in conjunction with AWS.
The following is what the cloudMQTT setup page looks like for an individual instance.

<img width="922" alt="cloudMQTT" src="https://user-images.githubusercontent.com/60630614/91782135-44e4fc00-ebca-11ea-806f-26748cc1bc9f.png">

The important parts of data to note from your message or cloud broker is the user data (username, and password), the port, and server.
Other information may  be needed depending on how advanced of a project you're using a cloud broker to implement. 

To use a message broker, you need to purchase access to a cloud broker, or go through the message broker of your choice and choose a plan. Then creating a new instance is relatively easy once you choose a plan right for your project. 

## Creating the Client Code
Many mqtt libraries can be downloaded in order to publish and recieve messages from whichever topics you subscribe to. In the case of this project, I used the eclipse paho library.
https://pypi.org/project/paho-mqtt/#client

Install the eclipse paho library on your IDE of choice, then create a new python file and import the paho mqtt library by using 

```
import paho.mqtt.client as mqtt
```
in the header of your code file. 

We are also looking to publish data to a certain topic. In order to do that we need to import another part of the paho mqtt library. Below the code line above, add
```
import paho.mqtt.publish as publish
```
Following eclipse paho literature found on their website and their github, to publish ome message, the following function can be used.
```
#example_topic is topic to subscribe to
#payload is what you want the topic to display
#qos, options either 0,1,2, defaults to 0
#hostname is broker http
#port is the internet port using through cloud broker
#client-id should be populated from client app
#auth are account permissions
#protocol is the mqtt version, in this case 3.1.1

example_topic = ""
publish.single(example_topic, payload=None, qos=0, retain=False, hostname="",
                port= , client_id="", keepalive=60, 
                will=None, auth={'username':"", 'password':""}, tls=None,
                protocol=mqtt.MQTTv311, transport="tcp")
```
With the user filling in their own cloud broker username, password, hostname, and port number.

To publush multiple messages, the following function can be used.
```
#topic is topic to subscribe to, in this example "paho/test/multiple"
#payload is what you want the topic to display, two different messages in this example
#qos, options either 0,1,2, defaults to 0
#retain is false in this case because we don't want the message retained after our instance is done
#hostname is broker http
#port is the internet port using through cloud broker
#client-id should be populated from client app
#auth are account permissions
#protocol is the mqtt version, in this case 3.1.1

msgs = [{'topic':"paho/test/multiple", 'payload':"multiple 1"},
    ("paho/test/multiple", "multiple 2", 0, False)]

publish.multiple(msgs, hostname="tailor.cloudmqtt.com", port= , client_id=" ", keepalive=60,
    will=None, auth={'username':" ", 'password':" "}, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
 ```
