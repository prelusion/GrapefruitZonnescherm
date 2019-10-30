#include "manual.h"
#include <avr/eeprom.h>

// The manual configuration will be stored in EEPROM at address 0x0008.
#define MANUAL_ADDRESS 0x0008

uint8_t get_manual(void)
{
	return eeprom_read_byte((uint8_t*)MANUAL_ADDRESS);
}

void set_manual(uint8_t manual)
{
	eeprom_write_byte((uint8_t*)MANUAL_ADDRESS, manual);
}
