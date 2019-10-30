#include "unit_id.h"
#include <avr/eeprom.h>

// The unit will be stored in EEPROM at address 0x0000 and 0x0001.
#define UNIT_ID_ADDRESS 0x0000

uint16_t get_unit_id(void)
{
	return eeprom_read_word((uint16_t*)UNIT_ID_ADDRESS);
}

void set_unit_id(uint16_t unit_id)
{
	eeprom_write_word((uint16_t*)UNIT_ID_ADDRESS, unit_id);
}

uint8_t has_unit_id(void)
{
	return get_unit_id() != 0;
}