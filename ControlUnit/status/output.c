#include <avr/io.h>
#include "output.h"

//Sets the led ports
void init_leds(void)
{
	DDRB = 0b00000111;
	PORTB = 0x00;
}

//Controls the leds with the shutter status
void control_leds(ShutterStatus status)
{
	switch(status)
	{
		case CLOSED:
		//Makes the red led emit light consistently
		PORTB = 0b00000100;
		break;
		case OPEN:
		//Makes the green led emit light consistently
		PORTB = 0b00000010;
		break;
		//Checks if the red and yellow leds are already emitting light. If so stop. If not emit light.
		case CLOSING:
		PORTB = (~PORTB & 0b00000101);
		break;
		//Checks if the green and yellow leds are already emitting light. If so stop. If not emit light.
		case OPENING:
		PORTB = (~PORTB & 0b00000011);
		break;
	}
}

