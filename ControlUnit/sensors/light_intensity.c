#include <avr/io.h>

uint32_t lightlvl;
uint32_t lightintensity;
uint16_t min = 0;
uint16_t max = 800;
// Gets the lightintensity of the arduino and converts it to a %amount of light.
uint8_t get_light_intensity(void)
{
	//Gets the lightlvl of the assigned analog pin
	lightlvl = adc_read(PINC1);
	//Converts the light intensity to a %amount
	lightintensity = (((lightlvl - min) * 100) / (max - min));
	//If the lightlvl is above the max amount it can handle set the %amount to 100%
	if(lightlvl > max)
	{
		lightintensity = 100;
	}
	//Return the %amount
	return lightintensity;
}

uint8_t light_intensity_sensor_connected(void)
{
	return 1;
}