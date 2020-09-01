# Creating MQTT Client and Connecting to MQTT Broker
## Set up the cloud broker
For this project, I used cloudMQTT in conjunction with AWS.
The following is what the cloudMQTT setup page looks like for an individual instance.

<img width="922" alt="cloudMQTT" src="https://user-images.githubusercontent.com/60630614/91782135-44e4fc00-ebca-11ea-806f-26748cc1bc9f.png">

The important parts of data to note from your message or cloud broker is the user data (username, and password), the port, and server.
Other information may  be needed depending on how advanced of a project you're using a cloud broker to implement. 

To use a message broker, you need to purchase access to a cloud broker, or go through the message broker of your choice and choose a plan. Then creating a new instance is relatively easy once you choose a plan right for your project. 

## Creating the Client Code
https://pypi.org/project/paho-mqtt/#client
