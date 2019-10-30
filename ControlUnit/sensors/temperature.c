#include <avr/io.h>

uint8_t temperature;
int8_t get_temperature(void)
{
	temperature = ((adc_read(PINC0)*(5.0/1024.0))-0.5)*100;
	return temperature;
}

uint8_t temperature_sensor_connected(void)
{
	temperature = get_temperature();
	if (temperature > 63 || temperature < -64)
	{
		return 0;
	}
	return 1;
}
