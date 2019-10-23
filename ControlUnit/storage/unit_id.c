#include <avr/eeprom.h>

// The unit will be stored in EEPROM at address 0x0000 and 0x0001.
#define unit_id_address 0x0000

uint16_t get_unit_id()
{
	return eeprom_read_word((uint16_t*)unit_id_address);
}

void set_unit_id(uint16_t unit_id)
{
	eeprom_write_word((uint16_t*)unit_id_address, unit_id);
}

uint8_t has_unit_id()
{
	return get_unit_id() != (uint16_t)0;
}