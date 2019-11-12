#ifndef _STATUS_OUTPUT_H_
#define _STATUS_OUTPUT_H_

#include "../data.h"
#include <stdint.h>


/** 
 * \brief  
 * displays the measurement on the digital display
 */ 
 void display_measurement(SelectedSensor sensor, int16_t measurement);
 
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
 SelectedSensor check_new_pressed_buttons_from_display(void);
 
/**
 * \brief 
 * Checks a new pressed button.
 * 
 * \returns the pressed new button
 */
 SelectedSensor read_pressed_display_buttons(void);
 
 #endif