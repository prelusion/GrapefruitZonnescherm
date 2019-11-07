#include "shutter.h"
#include <avr/eeprom.h>

// The shutter status will be stored in EEPROM at address 0x0009.
#define SHUTTER_STATUS_ADDRESS 0x0009

uint16_t get_shutter_status(void)
{
	return eeprom_read_byte((uint8_t*)SHUTTER_STATUS_ADDRESS);
}

void set_shutter_status(uint8_t status)
{
	eeprom_write_byte((uint8_t*)SHUTTER_STATUS_ADDRESS, status);
}
