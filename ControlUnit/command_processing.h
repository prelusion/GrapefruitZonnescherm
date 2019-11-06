#ifndef _COMMAND_PROCESSING_H_
#define _COMMAND_PROCESSING_H_

#include <stdint.h>

typedef struct {
	char name[20];				// The command name. Max 20 characters.
	void(*function)(char[30], char[50]);	// Pointer to function that is associated with the command name.
	uint8_t parameters_required;
} Command;

/**
 * \brief 
 * Get all available commands.
 * 
 * \return Command* Collection of available commands
 */
Command* get_available_commands(void);


/**
 * \brief 
 * Process the provided input.
 *
 * \param input The input to process.
 */
void process_input(char* input);

/**
 * \brief 
 * Execute a command.
 * 
 * \param name The command name
 * \param parameters The command parameters
 */
void execute_command(char name[20], char parameters[30]);

void cmd_ping(char parameters[30], char result[50]);
void cmd_initialize(char parameters[30], char result[50]);
void cmd_reset(char parameters[30], char result[50]);
void cmd_get_id(char parameters[30], char result[50]);
void cmd_set_id(char parameters[30], char result[50]);
void cmd_get_window_height(char parameters[30], char result[50]);
void cmd_set_window_height(char parameters[30], char result[50]);
void cmd_get_temperature_threshold(char parameters[30], char result[50]);
void cmd_set_temperature_threshold(char parameters[30], char result[50]);
void cmd_get_light_intensity_threshold(char parameters[30], char result[50]);
void cmd_set_light_intensity_threshold(char parameters[30], char result[50]);
void cmd_get_manual(char parameters[30], char result[50]);
void cmd_set_manual(char parameters[30], char result[50]);
void cmd_get_sensor_data(char parameters[30], char result[50]);
void cmd_get_sensor_history(char parameters[30], char result[50]);
void cmd_roll_up(char parameters[30], char result[50]);
void cmd_roll_down(char parameters[30], char result[50]);

#endif