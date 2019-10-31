#include "command_processing.h"
#include <string.h>
#include <stdlib.h>
#include <avr/io.h>
#include <stdio.h>
#include "data.h"

// Storage includes.
#include "storage/unit_id.h"
#include "storage/window_height.h"
#include "storage/temperature_threshold.h"
#include "storage/light_intensity_threshold.h"
#include "storage/history.h"
#include "storage/manual.h"

// Predefined command amount.
#define COMMAND_AMOUNT 15

Command* get_available_commands()
{
	Command* available_commands = malloc(COMMAND_AMOUNT * sizeof(Command));
	
	strcpy(available_commands[0].name, "PING");
	available_commands[0].function = &cmd_ping;
	
	strcpy(available_commands[1].name, "GET_ID");
	available_commands[1].function = &cmd_get_id;
	
	strcpy(available_commands[2].name, "SET_ID");
	available_commands[2].function = &cmd_set_id;
	
	strcpy(available_commands[3].name, "GET_WINDOW_HEIGHT");
	available_commands[3].function = &cmd_get_window_height;
	
	strcpy(available_commands[4].name, "SET_WINDOW_HEIGHT");
	available_commands[4].function = &cmd_set_window_height;
	
	strcpy(available_commands[5].name, "GET_TEMP_THRESHOLD");
	available_commands[5].function = &cmd_get_temperature_threshold;
	
	strcpy(available_commands[6].name, "SET_TEMP_THRESHOLD");
	available_commands[6].function = &cmd_set_temperature_threshold;
	
	strcpy(available_commands[7].name, "GET_LI_THRESHOLD");
	available_commands[7].function = &cmd_get_light_intensity_threshold;
	
	strcpy(available_commands[8].name, "SET_LI_THRESHOLD");
	available_commands[8].function = &cmd_set_light_intensity_threshold;
	
	strcpy(available_commands[9].name, "GET_MANUAL");
	available_commands[9].function = &cmd_get_manual;
	
	strcpy(available_commands[10].name, "SET_MANUAL");
	available_commands[10].function = &cmd_set_manual;
	
	strcpy(available_commands[11].name, "GET_SENSOR_DATA");
	available_commands[11].function = &cmd_get_sensor_data;
	
	strcpy(available_commands[12].name, "GET_SENSOR_HISTORY");
	available_commands[12].function = &cmd_get_sensor_history;
	
	strcpy(available_commands[13].name, "ROLL_UP");
	available_commands[13].function = &cmd_roll_up;
	
	strcpy(available_commands[14].name, "ROLL_DOWN");
	available_commands[14].function = &cmd_roll_down;
	
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
	} else {
		// Replace the = character with a null character so the input will be the command name.
		*startOfParameters = '\0';
		
		execute_command(input, startOfParameters + 1);
	}
}

void execute_command(char name[20], char* parameters)
{
	Command* commands = get_available_commands();
	
	for (uint8_t i = 0; i < COMMAND_AMOUNT; i++)
	{
		Command command = commands[i];
		
		if (strcmp(command.name, name) == 0)
		{
			char* result = command.function(parameters);
			printf("%s=%s\n", name, result);
			
			// Result has been returned so we can free it :D
			free(result);
		}
	}
	
	// TODO load available commands only once
	free(commands);
}

char* cmd_ping(char* parameters)
{
	char* result = malloc(5);
	strcpy(result, "PONG");
	
	return result;
}

char* cmd_get_id(char* parameters)
{
	char* result = malloc(11);
	sprintf(result, "%lu", get_unit_id());
	
	return result;
}

char* cmd_set_id(char* parameters)
{
	uint32_t unit_id = atol(parameters);
	char* result = malloc(6);
	
	if (unit_id)
	{
		set_unit_id(unit_id);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
	
	return result;
}

char* cmd_get_window_height(char* parameters)
{
	char* result = malloc(6);
	sprintf(result, "%u", get_window_height());
	
	return result;
}

char* cmd_set_window_height(char* parameters)
{
	uint16_t window_height = atoi(parameters);
	char* result = malloc(6);
	
	if (window_height)
	{
		set_window_height(window_height);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
	
	return result;
}

char* cmd_get_temperature_threshold(char* parameters)
{
	char* result = malloc(5);
	sprintf(result, "%d", get_temperature_threshold());
	
	return result;
}

char* cmd_set_temperature_threshold(char* parameters)
{
	int8_t temperature_threshold = atoi(parameters);
	char* result = malloc(6);
	
	if (temperature_threshold)
	{
		set_temperature_threshold(temperature_threshold);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
	
	return result;
}

char* cmd_get_light_intensity_threshold(char* parameters)
{
	char* result = malloc(4);
	sprintf(result, "%u", get_light_intensity_threshold());
	
	return result;
}

char* cmd_set_light_intensity_threshold(char* parameters)
{
	uint8_t light_intensity_threshold = atoi(parameters);
	char* result = malloc(6);
	
	if (light_intensity_threshold)
	{
		set_light_intensity_threshold(light_intensity_threshold);
		strcpy(result, "OK");
	}
	else
	{
		strcpy(result, "ERROR");
	}
	
	return result;
}

char* cmd_get_manual(char* parameters)
{
	char* result = malloc(4);
	sprintf(result, "%u", get_manual());
	
	return result;
}

char* cmd_set_manual(char* parameters)
{
	set_manual(atoi(parameters));
	char* result = malloc(3);
	strcpy(result, "OK");
	
	return result;
}

char* cmd_get_sensor_data(char* parameters)
{
	char* result = malloc(16);
	
	int8_t current_temperature = get_current_temperature();
	uint8_t current_light_intensity = get_current_light_intensity();
	ShutterStatus current_shutter_status = get_current_shutter_status();
	
	sprintf(result, "%d,%u,%u", current_temperature, current_light_intensity, current_shutter_status);
	
	return result;
}

char* cmd_get_sensor_history(char* parameters)
{
	char* result = malloc(16);
	strcpy(result, "NOT_IMPLEMENTED");
	
	return result;
}

char* cmd_roll_up(char* parameters)
{
	char* result = malloc(16);
	strcpy(result, "NOT_IMPLEMENTED");
	
	return result;
}

char* cmd_roll_down(char* parameters)
{
	char* result = malloc(16);
	strcpy(result, "NOT_IMPLEMENTED");
	
	return result;
}
