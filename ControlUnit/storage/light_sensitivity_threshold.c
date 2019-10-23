#include <avr/eeprom.h>

// The light sensitivity threshold will be stored in EEPROM at address 0x0005.
#define light_sensitivity_threshold_address 0x0005

uint8_t get_light_sensitivity_threshold()
{
	return eeprom_read_byte((uint8_t*)light_sensitivity_threshold_address);
}

void set_light_sensitivity_threshold(uint8_t light_sensitivity_threshold)
{
	eeprom_write_byte((uint8_t*)light_sensitivity_threshold_address, light_sensitivity_threshold);
}
