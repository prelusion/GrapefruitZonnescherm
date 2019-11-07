#include "status.h"
#include <avr/io.h>
#include <stdio.h>
#include "../data.h"

void init_leds(void)
{
	DDRB = 0b00000111;
	PORTB = 0x00;
}

void update_leds(void)
{
	switch(get_current_shutter_status())
	{
		case CLOSED:
			// Enable the red LED.
			PORTB = 0b00000100;
			break;
		case OPEN:
			// Enable the green LED.
			PORTB = 0b00000010;
			break;
		case CLOSING:
			// Blink the red and yellow LEDs.
			PORTB =(~PORTB & 0b00000101);
			break;
		case OPENING:
			// Blink the green and yellow LEDs.
			PORTB = (~PORTB & 0b00000011);
			break;
	}
}

