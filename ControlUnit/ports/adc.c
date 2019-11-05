#include <avr/io.h>

//Initialize ADC
void adc_init()
{
	
	//The REFS0, REFS1 bit of ADMUX is the voltage amount and how
	//ADLAR shows the result of the ADC
	//MUX Chooses the Analog pin on the arduino
	ADMUX = _BV(REFS0);
	//ADEN enables the ADC conversion (DOESNT START THE PROCES)
	//ADPS(n) sets a prescaler to change the frequency
	ADCSRA = _BV(ADEN)|_BV(ADPS0)|_BV(ADPS1)|_BV(ADPS2);
}

//Starts the ADC conversion 
//Always has to be called after a conversion is done
void start_conversion()
{
 	ADCSRA |= _BV(ADSC);
}

//Waits until the ADC conversion is done.
void waitout_conversion()
{
	while( (ADCSRA & _BV(ADSC)) != 0);	
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