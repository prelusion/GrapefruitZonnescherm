#include <avr/io.h>

int8_t get_temperature(void)
{
	//calculates the correct temperature with the following formula
	uint8_t temperature = ((adc_read(PINC0)*(5.0/1024.0))-0.5)*100;
	return temperature;
}

//If the temperature is not within the threshold return 0 else return 1
uint8_t temperature_sensor_connected(void)
{
	uint8_t temperature = get_temperature();
	if (temperature > 63 || temperature < -64)
	{
		return 0;
	}
	return 1;
}
