#include <avr/io.h>

uint8_t lightintensity;
uint8_t min = 0;
uint8_t max = 255;
uint8_t get_light_intensity(void)
{
	
	lightintensity = ((adc_read(PINC1) - min) * 100) / (max - min);
	printf("%u lightintensity \n", lightintensity);
	
	return 1;
}

uint8_t light_intensity_sensor_connected(void)
{	
	return 1;
}