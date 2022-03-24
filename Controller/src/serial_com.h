#ifndef SERIAL_COM_H
#define SERIAL_COM_H

#include "movement.h"
#include "encoder.h"

#include "BluetoothSerial.h"
BluetoothSerial SerialBT;
String input_serial;


void receive(){
  if (SerialBT.available()){
    input_serial = SerialBT.readStringUntil('/');
    //SerialBT.print("mensaje: ");
    //SerialBT.println(inputBT);
  }
  if (Serial.available()){
    input_serial = Serial.readStringUntil('/');
    //SerialBT.print("mensaje: ");
    //SerialBT.println(inputBT);
  }
}


void commands(String input_commands){

    if(input_commands.substring(0,5)=="MOVE:"){
        bool dir;
        String input=input_commands.substring(5);
        int first_sep=input.indexOf(";");
        int second_sep=input.indexOf(";",first_sep+1);

        String direction = input.substring(0,first_sep);
        if(direction=="0"){
            dir=0;
        }
        if(direction=="1"){
            dir=1;
        }
        float dis = input.substring(first_sep+1,second_sep).toFloat();
        float time = input.substring(second_sep+1).toFloat();

        trajectory(dir,dis,time);

        /*Serial.print("Dir: ");
        Serial.println(dir);
        Serial.print("dis: ");
        Serial.print(dis);
        Serial.println(" mm");
        Serial.print("time: ");
        Serial.print(time);
        Serial.println(" mm/s");
        */
        }

    if(input_commands=="POS"){
      float pos=((int32_t)encoder.getCount())/100; //mm
      Serial.print("POS: ");
      Serial.print(pos);
      Serial.println(" mm");
    }


}



#endif