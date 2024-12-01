this script utilises:-

+ Pico WH (any pico should suffice)
+ Micro PIR Motion Sensor (WPSE353) by Velleman
+ A photoresistor / light-dependent resistor (LDR)
+ LED Strip - i've used the 66 star on from piromoni (at 40%)

it senses motion using the PIR and if the location is dark (set by a threshold) it then fades the led strip in,
It keeps the led strip on for 20seconds, checks the PIR again, if motion is still detected, it adds a further 20 seconds on to the timeout.
if no motion is detected, it fades the LED strip out.

this is useful for lighting up corridors or hallways
