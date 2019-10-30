#include <avr/io.h>

//Initialize ADC
void adc_init() {
	
	//The REFS0, REFS1 bit of ADMUX is the voltage amount and how
	//ADLAR shows the result of the ADC
	//MUX Chooses the Analog pin on the arduino
	ADMUX = (0 << REFS1)|(1 << REFS0)|(0 << ADLAR)|(0 << MUX2)|(0 << MUX1)|(0 << MUX0);
	/*  (1 << MUX3)|(0 << MUX2)|(0 << MUX1)|(0 << MUX0)  */
	//ADEN enables the ADC conversion (DOESNT START THE PROCES)
	//ADPS(n) sets a prescaler to change the frequency
	ADCSRA = (1 << ADEN)|(1 << ADPS0)|(1 << ADPS1)|(1 << ADPS2);
}

//Starts the ADC conversion 
//Always has to be called after a conversion is done
void start_conversion() {
 	ADCSRA |= (1 << ADSC);
}

//Waits until the ADC conversion is done.
void waitout_conversion() {
	while( (ADCSRA & (1 << ADSC)) != 0);	
}

//Reads the value of the open ADC
uint16_t adc_read(uint8_t ADCchannel)
{
	//Check if the right channels are selected
	ADMUX = (ADMUX & 0b11000000) | (ADCchannel & 0x0F);
	//Starts the ADC conversion
	start_conversion();
	// Loops as long as the conversion is running 
	waitout_conversion();
	return ADC;
}