#include "history.h"
#include <avr/eeprom.h>
#include <stdlib.h>

// The history start index will be stored in EEPROM at address 0x0006 and 0x0007.
#define HISTORY_START_INDEX_ADDRESS 0x0009

// The history start index will be stored in EEPROM at address 0x0008 and 0x0009.
#define HISTORY_SIZE_ADDRESS 0x000B

// The history will be stored in EEPROM at address 0x0020 until end of memory.
#define HISTORY_ADDRESS 0x0020

// TODO maybe there already is a definition of EEPROM size :)
#define EEPROM_END_ADDRESS 0x0400

void init_history(void)
{
	uint16_t size = eeprom_read_word((uint16_t*)HISTORY_SIZE_ADDRESS);
	
	// If the size is zero clear the history just to be sure.
	// When the size is larger then possible it must be invalid, so clear it.
	if (size == 0 || (size * 2) > EEPROM_END_ADDRESS - HISTORY_ADDRESS)
	{
		clear_history();
	}
}

History load_history(void)
{
	History history;
	
	// Read the size and start index from EEPROM.
	history.size = eeprom_read_word((uint16_t*)HISTORY_SIZE_ADDRESS);
	uint16_t start_index = eeprom_read_word((uint16_t*)HISTORY_START_INDEX_ADDRESS);
	
	// Allocate memory for the history data. This must be freed after use!
	history.data = (uint16_t*)malloc(history.size * 2);
	
	// Check if there is a "History overflow".
	if ((((uint16_t) HISTORY_ADDRESS) + (start_index * 2) + (history.size * 2)) > (uint16_t) EEPROM_END_ADDRESS)
	{
		// Check how much to read until the end of EEPROM.
		uint16_t read_to_end_size = ((uint16_t) EEPROM_END_ADDRESS) - ((uint16_t) HISTORY_ADDRESS) - (start_index * 2);
		
		// Read until end of EEPROM.
		eeprom_read_block(history.data, (const void*)(((uint16_t) HISTORY_ADDRESS) + (start_index * 2)), read_to_end_size);
		
		// Continue reading the remaining data from the start of EEPROM.
		eeprom_read_block(history.data + read_to_end_size, (const void*)(((uint16_t) HISTORY_ADDRESS)), (history.size * 2) - read_to_end_size);
	}
	else
	{
		// No overflow, we can just read the history starting at the first history_address.
		eeprom_read_block(history.data, (const void*)((uint16_t) HISTORY_ADDRESS), (history.size * 2));
	}
	
	return history;
}

void clear_history(void)
{
	// Reset the history start index to 0.
	eeprom_write_word((uint16_t*)HISTORY_START_INDEX_ADDRESS, (uint16_t)0);
	
	// Set the history size to 0.
	eeprom_write_word((uint16_t*)HISTORY_SIZE_ADDRESS, (uint16_t)0);
}

void write_measurement(uint16_t value)
{
	// Read the size and start index from EEPROM.
	uint16_t start_index = eeprom_read_word((uint16_t*) HISTORY_START_INDEX_ADDRESS);
	uint16_t size = eeprom_read_word((uint16_t*) HISTORY_SIZE_ADDRESS);
	
	// Check if there is a "History overflow".
	if (HISTORY_ADDRESS + (start_index * 2) + (size * 2) < EEPROM_END_ADDRESS)
	{
		eeprom_write_word((uint16_t*) (HISTORY_ADDRESS + (start_index * 2) + (size * 2)), value);
		eeprom_write_word((uint16_t*) HISTORY_SIZE_ADDRESS, size + 1);
	}
	else
	{
		eeprom_write_word((uint16_t*) (HISTORY_ADDRESS + (start_index * 2)), value);
		eeprom_write_word((uint16_t*) HISTORY_START_INDEX_ADDRESS, start_index == (size - 1) ? 0 : (start_index + 1));
	}
}