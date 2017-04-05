// demo: CAN-BUS Shield, send data
#include <mcp_can.h>
#include <SPI.h>

// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;
const int ledHIGH    = 1;
const int ledLOW     = 0;

const int ENGINE_SIGNALS_ID = 0x100;
const int WARNINGS_ID = 0x200;
const int ELECTRICAL_SYSTEMS_ID = 0x300;
const int CONTROL_ID = 0x400;


MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin

void setup()
{
    Serial.begin(115200);

    while (CAN_OK != CAN.begin(CAN_500KBPS))              // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init fail");
        Serial.println(" Init CAN BUS Shield again");
        delay(100);
    }
    Serial.println("CAN BUS Shield init ok!");
}


uint8_t coolant = 10;
uint8_t torque = 20;
uint8_t rpm1 = 10;
uint8_t rpm2 = 0;
uint8_t throttle = 40;
uint8_t warnings = 0;

uint8_t ess_soc = 10;
uint8_t ess_voltage = 10;

uint8_t current_cont = 0;
uint8_t current_gear = 1;
uint8_t vehicle_speed = 30;
uint8_t energy_ab = 10;


unsigned char engineSignals[5] = {0, 0, 0, 0, 0};
unsigned char warningSignals[1] = {0};
unsigned char electricalSignals[2] = {0,0};
unsigned char controlSignals[4] = {0,0,0};

void loop()
{   Serial.println("In loop");
    // send data:  id = 0x00, standard frame, data len = 8, stmp: data buf
    CAN.sendMsgBuf(ENGINE_SIGNALS_ID,0, 8, engineSignals);
    CAN.sendMsgBuf(WARNINGS_ID,0, 8, warningSignals);
	CAN.sendMsgBif(ElECTRICAL_SYSTEMS_ID, 0, 8, electricalSignals);
	CAN.sendMsgBif(CONTROL_ID, 0, 8, controlSignals);
	electricalSignals[0] = ess_soc++;
	electricalSiganls[1] = ess_volatage++;
	controlSignals[0] = curr_cont++;
	controlSignals[0] = current_gear++;
	controlSignals[1] = vehicle_speed++;
	controlSignals[2] = energy_ab++;
	warningSignals[0] = warnings++;
    engineSignals[0] = coolant++;
    engineSignals[1] = torque++;
    engineSignals[2] = rpm1++;
    engineSignals[3] = rpm2++;
    engineSignals[4] = throttle++;
    
    
    delay(1000);                       // send data once per second
}
/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
