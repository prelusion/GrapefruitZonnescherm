#ifndef _STATUS_SHUTTER_H_
#define _STATUS_SHUTTER_H_

#include <stdint.h>
#include "../data.h"

/** 
 * \brief  
 * Initializes the shutter status at startup
 */ 
void init_shutter_status(void); 

/** 
 * \brief  
 * Checks if the next shutter status should be open or closed.
 * After checks set the right shutter status and update leds.
 */
void control_shutter(void);
/** 
 * \brief  
 * Removes last shutter task and starts a roll_up task
 */
void shutter_roll_up(void);

/** 
 * \brief
 * Removes last shutter task and starts a roll_down task
 */
void shutter_roll_down(void);

#endif