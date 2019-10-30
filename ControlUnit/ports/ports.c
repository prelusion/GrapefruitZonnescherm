#include <avr/io.h>

//Sets I/O on the right pins
void init_ports()
{
	DDRD = 0b11100000;
	PINB = 0b11000000; 
}