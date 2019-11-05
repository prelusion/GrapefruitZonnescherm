#include <avr/io.h>

//Sets I/O on the right pins
void init_ports()
{
	DDRB = 0b00000111;
	PORTB = 0b00000111;
	
	//Set all pins except pin 7 to output
	DDRD = 0b01010000;
	//Disables all pins
	PORTD = 0x00;
}