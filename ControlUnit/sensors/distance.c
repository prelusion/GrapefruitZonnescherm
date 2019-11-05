#include "distance.h"

#define F_CPU 16000000UL

#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

uint8_t echo_received = 0;

ISR(INT1_vect)
{
	if ((PIND & _BV(PORTD3)) == _BV(PORTD3))
	{
		TCCR1B = _BV(CS11);   // Set prescaling to 8.
		TIMSK1 = _BV(OCIE2A); // Timer 2 Output Compare A Match Interrupt Enable
		TCNT1 = 0;
		echo_received = 1;
	}
	else
	{
		TCCR1B = 0;
	}
}

void init_distance_sensor(void)
{
	EICRA = _BV(ISC10); // Any logical change on INT1 generates an interrupt request.
	EIMSK = _BV(INT1); // Enable INT1 interupts.
	
	// Set output.
	DDRD |= _BV(PORTD4); // Set pin 4 as output.
	DDRD &= ~_BV(PORTD3); // Set pin 3 as input.
}

uint16_t get_distance(void)
{
	echo_received = 0;
	
	// Generate a 10us pulse to the trigger port.
	PORTD |= _BV(PORTD4);
	_delay_us(10);
	PORTD &= ~_BV(PORTD4);
	
	// Wait for the echo.
	_delay_us(500);
	
	// Check if an echo has been received after 500ug.
	if (!echo_received)
	{
		// When there is no echo the sensor probably isn't connected properly.
		TCCR1B = 0;
		return 0;
	}
	
	// Wait until the echo stops.
	while (TCCR1B != 0);
	
	// Prescaling is set to 8. So the timer will increase 2,000,000 timer per second. That is once every 0.5ug.
	// To calculate the distance in CM we need to divide the amount of ug with 58, because the timer is increased every 0.5ug we need to divide the counter value with 116.
	return (TCNT1 / 116);
}

uint8_t distance_sensor_connected(void)
{
	return (uint8_t)get_distance();
}
