#ifndef _OUTPUT_STATUS_H_
#define _OUTPUT_STATUS_H_

#include "../data.h"

/** 
 * \brief  
 * Sets specific ports to output for the leds.
 */ 
void init_leds(void); 
 
/** 
 * \brief  
 * Let the leds glow when its needed.
 */ 
void update_leds(void); 
 
 #endif