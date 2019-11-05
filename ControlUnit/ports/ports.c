#include <avr/io.h>

//Sets I/O on the right pins
void init_ports()
{
	DDRB = 0b00000111;
	PORTB = 0b00000111;
}