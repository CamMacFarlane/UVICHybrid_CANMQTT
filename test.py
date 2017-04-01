import can
import paho.mqtt.publish as publish

HOST = "10.42.0.1"
PORTNUM = 1884

THROTTLE_PRESSURE_ID = 0x0070
BRAKE_PRESSURE_ID = 0x0080
ENGINE_TEMP_ID = 0x0010

IDtoTopic = {
    THROTTLE_PRESSURE_ID : 'throttle_pressure',
    BRAKE_PRESSURE_ID : 'brake_pressure',
    ENGINE_TEMP_ID : 'engine_temp',
    
}

def processMessage(msg):
    id = message.arbitration_id
    topic = IDtoTopic.get(id, "error")
    print(topic)
    print(message.data)
    for i in range(0, message.dlc):

        publishData(bin(message.data[i]), topic)    

def publishData(data, topic):
    publish.single("CANDUMP", data, hostname=HOST ,port=PORTNUM)
    publish.single(topic, data, hostname=HOST, port=PORTNUM)

can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan_native')
message = bus.recv(1.0)  # Timeout in seconds.

if message is None:
    print('Timeout occurred, no message.')
else:
    print(message)
    processMessage(message)
    str = str(message.data)
    print(str)
