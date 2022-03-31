import mqtt_client
import rpi.amqp_client as amqp_client

# parameters
ip_rabbitmq = "192.168.1.7"
ip_broker_mqtt = "192.168.1.3"
topics_mqtt = "default_topic"

# connect to rabbitmq
amqp_channel = amqp_client.connect_to_rabbitmq(ip_rabbitmq)

# connect to mqtt broker and subscribe to topics
mqtt_client.message = None
mqttc = mqtt_client.connect(ip_broker_mqtt)
mqttc.subscribe(topics_mqtt)

# keep checking if new data arrived
mqttc.loop_start()
while True:
    if mqtt_client.message is not None:
        # retrieve topic and payload
        topic = mqtt_client.message
        payload = str(mqtt_client.message.payload.decode("utf-8"))
        # forward payload to amqp server
        amqp_client.send_message_to_rabbitmq(
            amqp_channel,
            payload,
        )
        # reset message
        mqtt_client.message = None