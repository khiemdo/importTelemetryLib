#include "mbed.h"
#include "telemetry/Telemetry.hpp"

//------------------------------------
// Hyperterminal configuration
// 9600 bauds, 8-bit data, no parity
//------------------------------------

DigitalOut myled(LED1);
Telemetry TM(115200);
Timer tm_timer;
AnalogIn analog_value(A0);
 
int main() {
  while(1) { 
    if(tm_timer.read_ms() > 50)
    {
        TM.pub_f32("touch",analog_value.read());
        myled = !myled;
        tm_timer.reset();
        TM.update();   
    }      
  }
}
 