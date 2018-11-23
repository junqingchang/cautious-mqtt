import paho.mqtt.client as mqtt
import time
import cmd
import sys
import select

username = "zf2sHjr"
broker = "test.mosquitto.org"
port = 1883
dchannels = ['hello/world', 'user/{}'.format(username)]


def on_connect(client, userdata, flags, rc):
    if rc == mqtt.MQTT_ERR_SUCCESS:
        print("Connected to {} with result code {}".format(broker, rc))
    for dc in dchannels:
        print("Subscribing to channel {}".format(dc))
        client.subscribe(dc, 1)


def on_message(client, userdata, msg):
    print("Message from {}: {}".format(msg.topic, msg.payload))


class cli(cmd.Cmd):
    """Simple MQTT chat client."""

    client = None
    looping = True

    def do_msg(self, person):
        "send hello message to user/<person>"
        if person:
            greeting = "hello {}".format(person)
        else:
            greeting = 'hello'
        print("Sending {} to {}".format(greeting, "user/{}".format(person)))
        mqttc = mqtt.Client("python_pub")
        mqttc.connect(broker, port)
        mqttc.publish("user/{}".format(person), greeting)
        mqttc.loop(2)

    def do_quit(self, line):
        "exit client"
        print("Goodbye!")
        exit(0)

    def do_subscribe(self, channel):
        "subscribe to <channel>"
        if channel:
            print("Subscribing to channel {}".format(channel))
            client.subscribe(channel, 1)
        else:
            print("No channel stated")

    def do_unsubscribe(self, channel):
        "unsubscribe to <channel>"
        if channel:
            print("Unsubscribing to channel {}".format(channel))
            client.unsubscribe(channel)
        else:
            print("No channel stated")


client = mqtt.Client(clean_session=False, client_id=username)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
time.sleep(1)

cli.client = client

print("Welcome to the MQTT client CLI. Type 'help' or 'msg <person>'")
while True:
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line:
            cli().onecmd(line)
        else:
            print('eof')
            exit(0)
    else:
        client.loop(1)
