#ifndef _STATUS_OUTPUT_H_
#define _STATUS_OUTPUT_H_
#include "../data.h"

/** 
 * \brief  
 * Sets specific ports to output for the leds 
 *  
 * Void no returns 
 */ 
void init_leds(void); 
 
/** 
 * \brief  
 * Let the lets glow when its needed 
 *  
 * Void no returns 
 */ 
void control_leds(ShutterStatus status); 

 
 #endif