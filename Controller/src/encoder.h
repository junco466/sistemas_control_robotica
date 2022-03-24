#ifndef ENCODER_H
#define ENCODER_H

#include <ESP32Encoder.h>

ESP32Encoder encoder;

unsigned long timer_encoder;

void encoder_(){
    if(millis()-timer_encoder>=1000){
  Serial.println("Encoder count = " + String((int32_t)encoder.getCount()));
  timer_encoder=millis();
   }
}
#endif