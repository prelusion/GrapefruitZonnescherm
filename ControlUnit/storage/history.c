#include "history.h"
#include <avr/eeprom.h>
#include <stdlib.h>

// The history start index will be stored in EEPROM at address 0x001C and 0x001D.
#define HISTORY_START_INDEX_ADDRESS 0x001C

// The history start index will be stored in EEPROM at address 0x001E and 0x001F.
#define HISTORY_SIZE_ADDRESS 0x001E

// The history will be stored in EEPROM at address 0x0020 until end of memory.
#define HISTORY_ADDRESS 0x0020

// The maximum amount of saved history.
#define MAX_HISTORY_SIZE 300

void init_history(void)
{
	uint16_t size = eeprom_read_word((uint16_t*)HISTORY_SIZE_ADDRESS);
	
	// If the size is zero clear the history just to be sure.
	// When the size is larger then possible it must be invalid, so clear it.
	if ((size == 0) || (size * 2) > MAX_HISTORY_SIZE)
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
	if ((start_index + history.size) > MAX_HISTORY_SIZE)
	{
		// Check how much to read until the maximum history size address is reached.
		uint16_t read_to_end_size = (MAX_HISTORY_SIZE - start_index) * 2;
		
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
	if ((start_index + size) >= MAX_HISTORY_SIZE)
	{
		eeprom_write_word((uint16_t*) (HISTORY_ADDRESS + (start_index * 2)), value);
		eeprom_write_word((uint16_t*) HISTORY_START_INDEX_ADDRESS, (start_index == (size - 1)) ? 0 : (start_index + 1));
	}
	else
	{
		eeprom_write_word((uint16_t*) (HISTORY_ADDRESS + (size * 2)), value);
		eeprom_write_word((uint16_t*) HISTORY_SIZE_ADDRESS, size + 1);
	}
}