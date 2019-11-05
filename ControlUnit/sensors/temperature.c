#include "temperature.h"
#include <avr/io.h>

int8_t get_temperature(void)
{
	return (int8_t)((adc_read(PINC0)*(5.0/1024.0))-0.5)*100;
}

//If the temperature is not within the threshold return 0 else return 1
uint8_t temperature_sensor_connected(void)
{
	int8_t temperature = get_temperature();
	
	return ((temperature > -64) && (temperature < 63));
}
