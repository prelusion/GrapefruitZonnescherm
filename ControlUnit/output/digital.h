#ifndef _STATUS_OUTPUT_H_
#define _STATUS_OUTPUT_H_

#include "../data.h"
#include <stdint.h>

typedef enum {
	TEMPERATURE = 0,
	LIGHT_INTENSITY = 1
} Sensor;

/** 
 * \brief  
 * The numberboard shows the current temperature
 */ 
void show_temperature_digital(uint8_t temperature); 
 
/** 
 * \brief  
 * The numberboard shows the current light intensity;
 */ 
void show_light_intensity_digital(uint8_t light_intensity); 
 
 #endif