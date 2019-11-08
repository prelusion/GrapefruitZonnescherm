#ifndef _STATUS_OUTPUT_H_
#define _STATUS_OUTPUT_H_

#include "../data.h"
#include <stdint.h>

typedef enum {
	TEMPERATURE = 0,
	LIGHT_INTENSITY = 1,
	DISTANCE = 2
} Sensor;

/** 
 * \brief  
 * displays the measurement on the digital display
 */ 
 void display_measurement(Sensor sensor, uint8_t measurement);
 
 
/** 
 * \brief  
 * Setups the digital display ports
 */ 
 void digital_setup(void);
 
 
/**
 * \brief 
 * Checks if a new button is pressed. Also checks if its a valid press if not return the same as last time
 * 
 * \returns the last valid pressed button
 */
 uint8_t check_new_pressed_buttons(void);
 

/**
 * \brief 
 * Checks a new pressed button.
 * 
 * \returns the pressed new button
 */
 uint8_t read_buttons();


/**
 * \brief 
 * Get the last pressed button
 * 
 * \returns last valid button
 */
 uint8_t get_toggled_buttons();
 
/** 
 * \brief  
 * Set new pressed button/
 *
 *\param new_toggled_buttons a new toggle button. 
 */

 void set_toggled_buttons(uint8_t new_toggled_buttons);
 
 #endif