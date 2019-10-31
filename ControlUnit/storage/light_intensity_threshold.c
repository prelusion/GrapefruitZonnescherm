#include "light_intensity_threshold.h"
#include <avr/eeprom.h>

// The light intensity threshold will be stored in EEPROM at address 0x0005.
#define LIGHT_INTENSITY_THRESHOLD_ADDRESS 0x0007

uint8_t get_light_intensity_threshold(void)
{
	return eeprom_read_byte((uint8_t*)LIGHT_INTENSITY_THRESHOLD_ADDRESS);
}

void set_light_intensity_threshold(uint8_t light_intensity_threshold)
{
	eeprom_write_byte((uint8_t*)LIGHT_INTENSITY_THRESHOLD_ADDRESS, light_intensity_threshold);
}
