#include "command_processing.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "data.h"


//status includes
#include "status/shutter.h"

// Storage includes.
#include "storage/unit_id.h"
#include "storage/window_height.h"
#include "storage/temperature_threshold.h"
#include "storage/light_intensity_threshold.h"
#include "storage/history.h"
#include "storage/manual.h"

// Predefined command amount.
#define COMMAND_AMOUNT 17

Command* get_available_commands()
{
	Command* available_commands = malloc(COMMAND_AMOUNT * sizeof(Command));
	
	strcpy(available_commands[0].name, "PING");
	available_commands[0].function = &cmd_ping;
	available_commands[0].parameters_required = 0;
	
	strcpy(available_commands[1].name, "INITIALIZE");
	available_commands[1].function = &cmd_initialize;
	available_commands[1].parameters_required = 1;
	
	strcpy(available_commands[2].name, "RESET");
	available_commands[2].function = &cmd_reset;
	available_commands[2].parameters_required = 0;
	
	strcpy(available_commands[3].name, "GET_ID");
	available_commands[3].function = &cmd_get_id;
	available_commands[3].parameters_required = 0;
	
	strcpy(available_commands[4].name, "SET_ID");
	available_commands[4].function = &cmd_set_id;
	available_commands[4].parameters_required = 1;
	
	strcpy(available_commands[6].name, "GET_WINDOW_HEIGHT");
	available_commands[6].function = &cmd_get_window_height;
	available_commands[6].parameters_required = 0;
	
	strcpy(available_commands[7].name, "SET_WINDOW_HEIGHT");
	available_commands[7].function = &cmd_set_window_height;
	available_commands[7].parameters_required = 1;
	
	strcpy(available_commands[8].name, "GET_TEMP_THRESHOLD");
	available_commands[8].function = &cmd_get_temperature_threshold;
	available_commands[8].parameters_required = 0;
	
	strcpy(available_commands[9].name, "SET_TEMP_THRESHOLD");
	available_commands[9].function = &cmd_set_temperature_threshold;
	available_commands[9].parameters_required = 1;
	
	strcpy(available_commands[10].name, "GET_LI_THRESHOLD");
	available_commands[10].function = &cmd_get_light_intensity_threshold;
	available_commands[10].parameters_required = 0;
	
	strcpy(available_commands[11].name, "SET_LI_THRESHOLD");
	available_commands[11].function = &cmd_set_light_intensity_threshold;
	available_commands[11].parameters_required = 1;
	
	strcpy(available_commands[12].name, "GET_MANUAL");
	available_commands[12].function = &cmd_get_manual;
	available_commands[12].parameters_required = 0;
	
	strcpy(available_commands[13].name, "SET_MANUAL");
	available_commands[13].function = &cmd_set_manual;
	available_commands[13].parameters_required = 1;
	
	strcpy(available_commands[14].name, "GET_SENSOR_DATA");
	available_commands[14].function = &cmd_get_sensor_data;
	available_commands[14].parameters_required = 0;
	
	strcpy(available_commands[15].name, "GET_SENSOR_HISTORY");
	available_commands[15].function = &cmd_get_sensor_history;
	available_commands[15].parameters_required = 0;
	
	strcpy(available_commands[16].name, "ROLL_UP");
	available_commands[16].function = &cmd_roll_up;
	available_commands[16].parameters_required = 0;
	
	strcpy(available_commands[17].name, "ROLL_DOWN");
	available_commands[17].function = &cmd_roll_down;
	available_commands[17].parameters_required = 0;
	
	return available_commands;
}

void process_input(char* input)
{
	// Find the location of the = character.
	char* startOfParameters = strchr(input, '=');
	
	if (!startOfParameters)
	{
		// When there is no = character there are no parameters, so we can use the entire input as command name.
		execute_command(input, "");
	}
	else
	{
		// Replace the = character with a null character so the input will be the command name.
		*startOfParameters = '\0';
		
		execute_command(input, startOfParameters + 1);
	}
	
	if (!get_current_serial_connection())
	{
		// When input is received the unit is connected with a serial connection.
		set_current_serial_connection(1);
	}
}

void execute_command(char name[20], char parameters[20])
{
	// TODO load available commands only once
	Command* commands = get_available_commands();
	
	for (uint8_t i = 0; i < COMMAND_AMOUNT; i++)
	{
		Command command = commands[i];
		
		if (strcmp(command.name, name) == 0)
		{
			char result[50]; // Result buffer.
			if (command.parameters_required && !strlen(parameters))
			{
				strcpy(result, "ERROR");
			} else {
				command.function(parameters, (char*)&result);
			}
			printf("%s=%s\n", name, result);
			free(commands);
			return;
		}
	}
	
	printf("%s=NOT_FOUND\n", name);
	free(commands);
}

void cmd_ping(char parameters[20], char result[50])
{
	strcpy(result, "PONG");
}

void cmd_initialize(char parameters[20], char result[50])
{
	if (get_current_unit_status() != INITIALIZING) {
		// Don't initialize the unit when it already is.
		strcpy(result, "ERROR");
		return;
	}
	
	char* parameter;
	
	parameter = strtok(parameters, ",");
	cmd_set_id(parameter, result);
	
	parameter = strtok(NULL, ",");
	cmd_set_temperature_threshold(parameter, result);
	
	parameter = strtok(NULL, ",");
	cmd_set_light_intensity_threshold(parameter, result);
	
	parameter = strtok(NULL, ",");
	cmd_set_manual(parameter, result);
	
	// If the last parameter contains a value the init was successful.
	if (parameter)
	{
		set_current_unit_status(OPERATING);
		strcpy(result, "OK");
	}
	else
	{
		cmd_reset(NULL, result);
		strcpy(result, "ERROR");
	}
}

void cmd_reset(char parameters[20], char result[50])
{
	set_unit_id(0);
	set_temperature_threshold(0);
	set_light_intensity_threshold(0);
	set_manual(0);
	set_window_height(0);
	clear_history();
	set_current_unit_status(INITIALIZING);
	
	strcpy(result, "OK");
}

void cmd_get_id(char parameters[20], char result[50])
{
	sprintf(result, "%lu", get_unit_id());
}

void cmd_set_id(char parameters[20], char result[50])
{
	uint32_t unit_id = atol(parameters);
	
	if (unit_id)
	{
		set_unit_id(unit_id);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
}

void cmd_get_window_height(char parameters[20], char result[50])
{
	sprintf(result, "%u", get_window_height());
}

void cmd_set_window_height(char parameters[20], char result[50])
{
	uint16_t window_height = atoi(parameters);
	
	if (window_height)
	{
		set_window_height(window_height);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
}

void cmd_get_temperature_threshold(char parameters[20], char result[50])
{
	sprintf(result, "%d", get_temperature_threshold());
}

void cmd_set_temperature_threshold(char parameters[20], char result[50])
{
	int8_t temperature_threshold = atoi(parameters);
	
	if (temperature_threshold)
	{
		set_temperature_threshold(temperature_threshold);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
}

void cmd_get_light_intensity_threshold(char parameters[20], char result[50])
{
	sprintf(result, "%u", get_light_intensity_threshold());
}

void cmd_set_light_intensity_threshold(char parameters[20], char result[50])
{
	uint8_t light_intensity_threshold = atoi(parameters);
	
	if (light_intensity_threshold)
	{
		set_light_intensity_threshold(light_intensity_threshold);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
}

void cmd_get_manual(char parameters[20], char result[50])
{
	sprintf(result, "%u", get_manual());
}

void cmd_set_manual(char parameters[20], char result[50])
{
	set_manual(atoi(parameters));
	strcpy(result, "OK");
}

void cmd_get_sensor_data(char parameters[20], char result[50])
{
	// When the unit is initializing sensor data cannot be read.
	if (get_current_unit_status() == INITIALIZING)
	{
		strcpy(result, "ERROR");
		return;
	}
	
	int8_t current_temperature = get_current_temperature();
	uint8_t current_light_intensity = get_current_light_intensity();
	ShutterStatus current_shutter_status = get_current_shutter_status();
	
	sprintf(result, "%d,%u,%u", current_temperature, current_light_intensity, current_shutter_status);
}

void cmd_get_sensor_history(char parameters[20], char result[50])
{
	History history = load_history();
	
	// Start with sending the history size.
	printf("GET_SENSOR_HISTORY=L%u\n", history.size);
	
	const uint8_t chunk_size = 5;
	uint8_t chunk_count = (history.size / chunk_size);
	uint8_t last_chunk_size = chunk_size;
	
	// Round up.
	if (history.size % chunk_count)
	{
		last_chunk_size = history.size % chunk_count;
		chunk_count++;
	}
	
	// Split the history in chunks.
	for (uint8_t chunk_index = 0; chunk_index < chunk_count; chunk_index++)
	{
		uint8_t current_chunk_size = (chunk_index == (chunk_count - 1)) ? last_chunk_size : chunk_size;
		
		// Reserve 50 bytes for the readings.
		char argument[50];
			
		for (uint8_t i = 0; i < current_chunk_size; i++)
		{
			uint16_t measurement = *(history.data + (chunk_index * chunk_size) + i);
			int8_t temperature = (int8_t)(((measurement & 0b1111111000000000) >> 9) | (measurement & 0b1000000000000000) >> 8);
			uint8_t light_intensity = (uint8_t)(((measurement & 0b0000000111111100) >> 2) * 2); // Light intensity is saved as divided by 2, so we have to multiply it again.
			uint8_t shutter_status = (uint8_t)(measurement & 0b0000000000000011);
			
			if (i == 0)
			{
				sprintf(argument, "%d,%u,%u", temperature, light_intensity, shutter_status);
			}
			else
			{
				sprintf(argument, "%s;%d,%u,%u", argument, temperature, light_intensity, shutter_status);
			}
		}
		
		printf("GET_SENSOR_HISTORY=%s\n", argument);
	}
	
	// Free the history data.
	free(history.data);
	
	// History has been sent so can be cleared.
	clear_history();
	
	strcpy(result, "OK");
}

void cmd_roll_up(char parameters[20], char result[50])
{
	if (!get_manual())
	{
		strcpy(result, "ERROR");
		return;
	}
	shutter_roll_up();
	strcpy(result, "OK");
}

void cmd_roll_down(char parameters[20], char result[50])
{
	if (!get_manual())
	{
		strcpy(result, "ERROR");
		return;
	}
	shutter_roll_down();
	strcpy(result, "OK");
}
