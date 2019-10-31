#ifndef _COMMAND_PROCESSING_H_
#define _COMMAND_PROCESSING_H_

typedef struct {
	char name[20];				// The command name. Max 20 characters.
	char*(*function)(char*);	// Pointer to function that is associated with the command name.
} Command;

/**
 * \brief 
 * Get all available commands.
 * 
 * \return Command* Collection of available commands
 */
Command* get_available_commands();


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
void execute_command(char name[20], char* parameters);


char* cmd_ping(char* parameters);
char* cmd_initialize(char* parameters);
char* cmd_reset(char* parameters);
char* cmd_get_id(char* parameters);
char* cmd_set_id(char* parameters);
char* cmd_get_window_height(char* parameters);
char* cmd_set_window_height(char* parameters);
char* cmd_get_temperature_threshold(char* parameters);
char* cmd_set_temperature_threshold(char* parameters);
char* cmd_get_light_intensity_threshold(char* parameters);
char* cmd_set_light_intensity_threshold(char* parameters);
char* cmd_get_manual(char* parameters);
char* cmd_set_manual(char* parameters);
char* cmd_get_sensor_data(char* parameters);
char* cmd_get_sensor_history(char* parameters);
char* cmd_roll_up(char* parameters);
char* cmd_roll_down(char* parameters);

#endif