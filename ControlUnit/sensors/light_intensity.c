#include "light_intensity.h"
#include "../ports/adc.h"
#include <avr/io.h>

const uint16_t MINIMUM_LIGHT_INTENSITY = 200;
const uint16_t MAXIMUM_LIGHT_INTENSITY = 1000;

// Gets the light_intensity of the arduino and converts it to a %amount of light.
uint8_t get_light_intensity(void)
{
	//Gets the light_level of the assigned analog pin
	uint16_t light_level = adc_read(PINC1);
	//Converts the light intensity to a %amount
	uint16_t light_intensity = (uint16_t)((((uint32_t)(light_level - MINIMUM_LIGHT_INTENSITY)) * 100) / (MAXIMUM_LIGHT_INTENSITY - MINIMUM_LIGHT_INTENSITY));
	//If the light_level is above the max amount it can handle set the %amount to 100%
	if (light_level > MAXIMUM_LIGHT_INTENSITY)
	{
		light_intensity = 100;
	}
	//Return the %amount
	return (uint8_t)light_intensity;
}

uint8_t light_intensity_sensor_connected(void)
{
	return 1;
}