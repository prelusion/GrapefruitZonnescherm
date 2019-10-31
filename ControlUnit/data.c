#include "data.h"
#include <avr/io.h>

int8_t current_temperature;
uint8_t current_light_intensity;
uint16_t current_distance;
ShutterStatus current_shutter_status;
UnitStatus current_unit_status;

int8_t get_current_temperature(void)
{
	return current_temperature;
}

void set_current_temperature(int8_t temperature)
{
	current_temperature = temperature;
}

uint8_t	get_current_light_intensity(void)
{
	return current_light_intensity;
}

void set_current_light_intensity(uint8_t light_intensity)
{
	current_light_intensity = light_intensity;
}

uint16_t get_current_distance(void)
{
	return current_distance;
}

void set_current_distance(uint16_t distance)
{
	current_distance = distance;
}

ShutterStatus get_current_shutter_status(void)
{
	return current_shutter_status;
}

void set_current_shutter_status(ShutterStatus shutter_status)
{
	current_shutter_status = shutter_status;
}

UnitStatus get_current_unit_status(void)
{
	return current_unit_status;
}

void set_current_unit_status(UnitStatus unit_status)
{
	current_unit_status = unit_status;
}