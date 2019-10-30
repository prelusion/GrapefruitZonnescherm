#include <avr/io.h>

void init_ports() {
	DDRD = 0b11100000;
	PINB = 0b11000000;
}