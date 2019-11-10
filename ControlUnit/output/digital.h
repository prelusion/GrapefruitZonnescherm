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
 void init_digital_display(void);
 
 
/**
 * \brief 
 * Checks if a new button is pressed. Also checks if its a valid press if not return the same as last time
 * 
 * \returns the last valid pressed button
 */
 uint8_t check_new_pressed_buttons_from_display(void);
 

/**
 * \brief 
 * Checks a new pressed button.
 * 
 * \returns the pressed new button
 */
 uint8_t read_pressed_display_buttons(void);

 
 #endif