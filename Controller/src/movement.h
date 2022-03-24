#ifndef MOVEMENT_H
#define MOVEMENT_H

#include <Arduino.h>
#include "encoder.h"

#define pul_pin 14
#define dir_pin 27

#define vel_max 6.6667 // mm/s = 200rpm

unsigned long timer_vel;
int sampling_time=5; // mS
int step_count=0;
int step_prev_count=0;
int sum_steps=0;
int counter=0;
float max_v=0;


void velocity(){
    
    if(millis()-timer_vel>=sampling_time){
        step_count=abs(step_prev_count-(int32_t)encoder.getCount());
        step_prev_count=(int32_t)encoder.getCount();
        sum_steps+=step_count;
        counter++;

        timer_vel=millis();
   }
   float sampling_number=50;
   if(counter>=sampling_number){
    
       float steps_prom = sum_steps/sampling_number;
       float dist_prom = steps_prom/100; //mm
       float time_prom = sampling_time*pow(10,-3); //s
       float vel = dist_prom/time_prom; //mm/s

        if(vel>max_v){
           max_v=vel;
       }

       Serial.print("VEL:");
       Serial.println(vel);
       //Serial.println(" mm/s");
       

       counter=0;
       sum_steps=0;

   }
}

void move(bool dir, int steps,float vel){
    // 0 -> CW
    // 1 -> CCW
    // vel -> mm/s
    // vel_max = 200rpm -> 6.667 mm/s

    float T = (1/(400*vel))*pow(10,6);

    if(dir==0){
        digitalWrite(dir_pin, LOW);
    }
    if(dir==1){
        digitalWrite(dir_pin, HIGH);
    }
    for(int i=0; i<=steps; i++){
        velocity();
           
        digitalWrite(pul_pin, HIGH);
        delayMicroseconds(T/2);
        digitalWrite(pul_pin, LOW);
        delayMicroseconds(T/2);
    }
}

void trajectory(bool dir, float dis, float time){
    //dis -> mm
    //time -> s

    int steps=(800*dis)/2;
    float vel=dis/time;
    move(dir,steps,vel);
}









#endif