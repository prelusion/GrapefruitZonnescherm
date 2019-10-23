#include <avr/eeprom.h>

// The temperature threshold will be stored in EEPROM at address 0x0004.
#define temperature_threshold_address 0x0004

int8_t get_temperature_threshold()
{
	return (uint8_t)eeprom_read_byte((uint8_t*)temperature_threshold_address);
}

void set_temperature_threshold(int8_t temperature_threshold)
{
	eeprom_write_byte((uint8_t*)temperature_threshold_address, (uint8_t)temperature_threshold);
}
