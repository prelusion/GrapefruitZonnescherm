#include <avr/io.h>

//Intialize ADC
void adc_init() {
	//Sets the analog pin 0 as a input 
	#define ADC_PIN 0;
	
	//The REFS0, REFS1 bit of ADMUX is the voltage amount and how
	//ADLAR shows the result of the ADC 
	//MUX Chooses the Analog pin on the arduino
	ADMUX = (1 << REFS1)|(1 << ADLAR)|(1 << REFS0)|(1 << MUX3);
	
	//Sets a prescaler to change the frequency
	ADCSRA = (1 << ADEN)|(1 << ADPS0)|(1 << ADPS1)|(1 << ADPS2);
}

//Starts the ADC conversion 
//Always has to be called after a conversion is done
void start_conversion() {
	ADCSRA |= (1 << ADSC);
}

//Reads the value of the open ADC
uint16_t adc_read(uint8_t adcp)
{
	ADMUX |= adcp;
	start_conversion();
	while( (ADCSRA & (1 << ADSC)) );
	return ADC;
}