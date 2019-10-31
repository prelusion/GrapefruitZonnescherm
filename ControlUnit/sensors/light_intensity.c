#include <avr/io.h>

// Gets the light_intensity of the arduino and converts it to a %amount of light.
uint8_t get_light_intensity(void)
{
	uint16_t min = 0;
	uint16_t max = 800;
	//Gets the light_level of the assigned analog pin
	uint32_t light_level = adc_read(PINC1);
	//Converts the light intensity to a %amount
	uint32_t light_intensity = (((light_level - min) * 100) / (max - min));
	//If the light_level is above the max amount it can handle set the %amount to 100%
	if(light_level > max)
	{
		light_intensity = 100;
	}
	//Return the %amount
	return light_intensity;
}

uint8_t light_intensity_sensor_connected(void)
{
	return 1;
}