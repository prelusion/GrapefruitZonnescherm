#include <avr/io.h>

void adc_init() {
	//The REFS0, REFS1 bit of ADMUX is the voltage amount and how
	//MUX Chooses the Analog pin on the arduino
	ADMUX = (1 << REFS1)|(1 << REFS0)|(1 << MUX3)
	
	//Sets a prescaler to change the frequency
	ADCSRA = (1 << ADEN)|(1 << ADPS0)|(1 << ADPS1)|(1 << ADPS2)
}

void start_conversion() {
	ADCSRA |= (1 << ADSC)
}

uint16_t adc_read(uint8_t ch)
{
	
}