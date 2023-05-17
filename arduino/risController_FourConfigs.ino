/* Phase shift configuration for RIS:
 * H,L,L,H --> 0 degree
 * L,H,H,L --> 180 degree
 * H,L,H,L --> 90 degree
 * L,H,L,H --> 270 degree
 * 
 */
#define numPins         4*9   //number of pins used
#define INTERVAL_TIME   1  // delay time between configs
#define numConfigs      4   // number of configs
#define numElements     9  // number of elements in RIS
#define ARRAY_SIZE      9   // array size of received buffer
#define BAUD_RATE       115200   //serial baud rate
//#define startIndex     0  //number of pins used


uint8_t Pins[numPins] = {2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37};
byte configs[numConfigs] = {B1001,B0101,B0110,B1010};
byte RFin_bytes [ARRAY_SIZE];

void setup() {
  // initialise rest
  initialisePins();
  Serial.begin(BAUD_RATE);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0; i < numElements; i++){
    assignModes(0, i*numConfigs);
  }
  delay(INTERVAL_TIME);
   for(int i=0; i < numElements; i++){
    assignModes(1, i*numConfigs);
  }
  delay(INTERVAL_TIME);
   for(int i=0; i < numElements; i++){
    assignModes(2, i*numConfigs);
  }
  delay(INTERVAL_TIME);
   for(int i=0; i < numElements; i++){
    assignModes(3, i*numConfigs);
  }
  delay(INTERVAL_TIME);

}

void initialisePins () {
  for (uint8_t i = 0; i < numPins; i++) { //for each pin
    pinMode (Pins[i], OUTPUT);       // set as output
  }
}

void assignModes(int seqConfig, uint8_t startIndex) {
  
  for(uint8_t i = startIndex; i < startIndex+numConfigs; i++){
    digitalWrite(Pins[i], bitRead(configs[seqConfig],i-startIndex));
//    Serial.print(Pins[i]);
//    Serial.println(bitRead(configs[seqConfig],i-startIndex));
  }
}
