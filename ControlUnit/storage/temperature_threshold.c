#include "temperature_threshold.h"
#include <avr/eeprom.h>

// The temperature threshold will be stored in EEPROM at address 0x0004.
#define TEMPERATURE_THRESHOLD_ADDRESS 0x0004

int8_t get_temperature_threshold(void)
{
	return (uint8_t)eeprom_read_byte((uint8_t*)TEMPERATURE_THRESHOLD_ADDRESS);
}

void set_temperature_threshold(int8_t temperature_threshold)
{
	eeprom_write_byte((uint8_t*)TEMPERATURE_THRESHOLD_ADDRESS, (uint8_t)temperature_threshold);
}
