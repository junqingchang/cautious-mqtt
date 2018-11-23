import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.connect("test.mosquitto.org", 1883)
mqttc.publish("hello/world", "Hello...........?", qos=1)
mqttc.loop(2)
