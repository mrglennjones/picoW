this script utilises:-

+ Pico WH (any pico should suffice) 
+ Micro PIR Motion Sensor (WPSE353) by Velleman
+ A photoresistor / light-dependent resistor (LDR)
+ A 10k Ohm resistor
+ LED Strip - i've used the 66 star one from piromoni (at 40%)
+ 9 female dupont cables / 3 for the PIR / 3 for the LDR / 3 for the LED Strip

it senses motion using the PIR and if the location is dark (set by a threshold) it then fades the led strip in to white at 40% brightness,
It keeps the led strip on for 20seconds, checks the PIR again, if motion is still detected, it adds a further 20 seconds on to the timeout.
if no motion is detected, it fades the LED strip out.

this is useful for lighting up corridors or hallways

wire up the LDR as shown here: http://www.robotplatform.com/electronics/photoresistor/photoresistor_1.html

![pirldr](https://github.com/user-attachments/assets/c3f54e70-30c0-4300-8592-10c99a97286e)
