import can
import paho.mqtt.publish as publish

HOST = "10.42.0.1"
PORTNUM = 1884

#CAN ID definitions 
ENGINE_SIGNALS_ID = 0x0070
WARNINGS_ID = 0x200
ELECTRICAL_SYSTEMS_ID = 0x300
CONTROL_ID = 0x400

KNOWN_TOPICS = {'engine_singals_messsage','warnings_message', 'electircal_systems_message', 'control_message'}

#translations from message CAN ID to MQTT topic
IDtoTopic = {
    ENGINE_SIGNALS_ID : 'engine_singals_messsage',
    WARNINGS_ID : 'warnings_message',
    ELECTRICAL_SYSTEMS_ID : 'electircal_systems_message',
    CONTROL_ID : 'control_message',
}

def two8BitTo16bit(byte1,byte2):
    return ((byte1<<8)|byte2)

def formatENGINE_SIGNALS(msg):
    stringData =  "Engine coolant = " + str(msg.data[0]) + " "
    stringData += "Engine Torque = " + str(msg.data[1]) + " "
    stringData += "Engine RPM = " + str(two8BitTo16bit(msg.data[2],msg.data[3])) + " "
    stringData += "Throttle Percent = " + str(msg.data[4]) + " "
    print("yes in here")
    return stringData

def formatKnownID(msg, ID):
    formattedData = "null"
    # print("id = " + str(ID))
    if(ID == ENGINE_SIGNALS_ID):
        formattedData = formatENGINE_SIGNALS(msg)
    return formattedData 

""" Takes a CAN message stuct and pulishes its data to the topic associated with its CAN ID if the CAN ID does not have an associated topic 
it is published to an UNKNOWN_ID_ topic """
def processMessage(msg):
    id = message.arbitration_id
    
    #get a MQTT topic from the message ID
    topic = IDtoTopic.get(id, "UNKNOWN_ID_" + str(id))
    
    #check if our topic is known and therefore can be formatted
    if(topic in KNOWN_TOPICS):
        dataString = formatKnownID(msg, id)
        publishData(dataString,topic)

    else:
        for i in range(0, message.dlc):
             publishData(hex(message.data[i]), topic)    

    print(topic)
    print(message.data)
    
def publishData(data, topic):
    # publish.single("CANDUMP", data, hostname=HOST ,port=PORTNUM)
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
