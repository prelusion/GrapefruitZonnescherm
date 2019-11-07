#ifndef _STORAGE_SHUTTER_H_
#define _STORAGE_SHUTTER_H_

#include <stdint.h>

/**
 * \brief 
 * Get the shutter status
 * 
 * \return uint8_t The shutter status in CM
 */
uint8_t get_shutter_status(void);

/**
 * \brief 
 * Set the shutter status
 * 
 * \param status The shutter status to set in CM
 */
void set_shutter_status(uint8_t status);

#endif