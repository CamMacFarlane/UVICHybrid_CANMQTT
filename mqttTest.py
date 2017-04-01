import paho.mqtt.publish as publish
import time

print("Sending 0...")
publish.single("ledStatus", "0", hostname="10.42.0.1",port=1884)

time.sleep(1)
print("Sending 1...")
publish.single("ledStatus", "1", hostname="10.42.0.1", port=1884)
