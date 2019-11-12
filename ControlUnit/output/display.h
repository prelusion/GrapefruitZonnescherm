#ifndef _OUTPUT_DISPLAY_H_
#define _OUTPUT_DISPLAY_H_

#include "../data.h"
#include <stdint.h>
 
/** 
 * \brief  
 * Setups the digital display ports
 */ 
 void init_display(void);

/** 
 * \brief  
 * displays the measurement on the digital display
 */ 
 void display_measurement(SelectedSensor sensor, int16_t measurement);
 
/**
 * \brief 
 * Checks if a new button is pressed. Also checks if its a valid press if not return the same as last time
 * 
 * \returns the last valid pressed button
 */
 SelectedSensor load_currently_selected_sensor(void);
 
/**
 * \brief 
 * Checks a new pressed button.
 * 
 * \returns the pressed new button
 */
 SelectedSensor read_pressed_display_buttons(void);
 
 #endif