#include "window_height.h"
#include <avr/eeprom.h>

// The window height will be stored in EEPROM at address 0x0002 and 0x0003.
#define WINDOW_HEIGHT_ADDRESS 0x0004

uint16_t get_window_height(void)
{
	return eeprom_read_byte((uint16_t*)WINDOW_HEIGHT_ADDRESS);
}

void set_window_height(uint16_t window_height)
{
	eeprom_write_byte((uint16_t*)WINDOW_HEIGHT_ADDRESS, window_height);
}
