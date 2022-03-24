#include <Arduino.h>
#include <ESP32Encoder.h>

#include "serial_com.h"

#include "movement.h"
float temp_0=0;
float temp=0;
float vel=0;

#include "encoder.h"
void setup() {
  Serial.begin(115200);
  pinMode(pul_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);

  // ****** BLuetooth ******
  SerialBT.begin("Controlador_NEMA");

  //******ENCODER**********
  ESP32Encoder::useInternalWeakPullResistors=UP;
  encoder.attachHalfQuad(12, 13);
  encoder.setCount(0);
  Serial.println("Encoder Start = " + String((int32_t)encoder.getCount()));
  timer_encoder=millis();
}

void loop() {

  //move(0,800,6.6667);
  //delay(5000);

  //encoder_();
  //velocity();
  receive();
  commands(input_serial);
  input_serial="."; 
  //move(1,3200,0);
  //delay(1000);
}