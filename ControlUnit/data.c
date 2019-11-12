#include "data.h"

uint8_t current_serial_connection = 0;
int8_t current_temperature = 0;
uint8_t current_light_intensity = 0;
ShutterStatus current_shutter_status = 0;
UnitStatus current_unit_status = STARTING;
SelectedSensor current_selected_sensor = TEMPERATURE;

uint8_t get_current_serial_connection(void)
{
	return current_serial_connection;
}

void set_current_serial_connection(uint8_t serial_connected)
{
	current_serial_connection = serial_connected;
}

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

SelectedSensor get_current_selected_sensor()
{
	return current_selected_sensor;
}

void set_current_selected_sensor(SelectedSensor selected_sensor)
{
	current_selected_sensor= selected_sensor;
}