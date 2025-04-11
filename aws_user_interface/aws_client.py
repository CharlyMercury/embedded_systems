from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3sgau4euce4dy-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "compu"
PATH_TO_CERTIFICATE = "C:\\Users\\carlo\\OneDrive\\Desktop\\Programacion-de-sistemas-embebidos\\aws_user_interface\\certificates\\device_cert.crt"
PATH_TO_PRIVATE_KEY = "C:\\Users\\carlo\\OneDrive\\Desktop\\Programacion-de-sistemas-embebidos\\aws_user_interface\\certificates\\private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "C:\\Users\\carlo\\OneDrive\\Desktop\\Programacion-de-sistemas-embebidos\\aws_user_interface\\certificates\\root.pem"
TOPIC = "led"
RANGE = 10


def subsciption_callback(topic, payload, dup, qos, retain, **kwargs):
    print("Subscription callback: topic='{}' payload='{}'".format(topic, payload.decode('utf-8')))
    # Add your logic to handle the received message here
    # For example, you can parse the payload and take action based on its contents 


# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available

subsciption = mqtt_connection.subscribe(
    topic="sensors",
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=subsciption_callback,
)

connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')

count = 0

for i in range (RANGE):
    count = (count + 1) % 2
    message = message = {
        "state": {
            "led": {
            "onboard": count
            }
        }
    }
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "led")
    t.sleep(10)
print('Publish End')



disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()