#include <avr/eeprom.h>

// The window height will be stored in EEPROM at address 0x0003.
#define window_height_address 0x0003

uint8_t get_window_height()
{
	return eeprom_read_byte((uint8_t*)window_height_address);
}

void set_window_height(uint8_t window_height)
{
	eeprom_write_byte((uint8_t*)window_height_address, window_height);
}
