#include <avr/io.h>
#include <avr/delay.h>
#include <avr/interrupt.h>

unsigned int Ctemp;
unsigned int Ftemp;

//Initialize ADC
void adc_init() {
	// Sets ADMUX to default
	ADMUX = 0xff;
	//ADEN enables the ADC conversion (DOESNT START THE PROCES)
	//ADPS(n) sets a prescaler to change the frequency
	ADCSRA = (1 << ADEN)|(1 << ADPS0)|(1 << ADPS1)|(1 << ADPS2);
	start_conversion();
}

//Starts the ADC conversion 
//Always has to be called after a conversion is done
void start_conversion() {
	printf("\n");
 	ADCSRA |= (1 << ADSC);
}

//Reads the value of the open ADC
uint16_t adc_read()
{
	//The REFS0, REFS1 bit of ADMUX is the voltage amount and how
	//ADLAR shows the result of the ADC
	//MUX Chooses the Analog pin on the arduino
	ADMUX = (1 << REFS1)|(1 << REFS0)|(0 << ADLAR)|(1 << MUX3)|(0 << MUX2)|(0 << MUX1)|(0 << MUX0);
	//Gives ADMUX the time to select the right channel
	_delay_us(10);
	start_conversion();
	
	// Loops as long as the conversion is running 
	while( (ADCSRA & (1 << ADSC)) != 0);
		
	Ctemp = (ADC - 247)/1.22;
	Ftemp = (Ctemp * 1.8);
	printf("%u Ctemp ", Ctemp);
	printf("\n");
	printf("%u Ftemp ", Ftemp);
	printf("\n");
	
	return ADC;
}