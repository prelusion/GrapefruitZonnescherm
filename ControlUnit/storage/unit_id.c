#include "unit_id.h"
#include <avr/eeprom.h>

// The unit will be stored in EEPROM at address 0x0000 until 0x0003.
#define UNIT_ID_ADDRESS 0x0000

uint32_t get_unit_id(void)
{
	uint32_t unit_id;
	eeprom_read_block(&unit_id, (uint32_t*)UNIT_ID_ADDRESS, 4);
	
	return unit_id;
}

void set_unit_id(uint32_t unit_id)
{
	eeprom_write_block(&unit_id, (uint32_t*)UNIT_ID_ADDRESS, 4);
}

uint8_t has_unit_id(void)
{
	return !get_unit_id();
}