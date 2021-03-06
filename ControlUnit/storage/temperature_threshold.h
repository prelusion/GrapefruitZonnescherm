#ifndef _STORAGE_TEMPERATURE_THRESHOLD_H_
#define _STORAGE_TEMPERATURE_THRESHOLD_H_

#include <stdint.h>

/**
 * \brief 
 * Get the current temperature threshold.
 * 
 * \return uint8_t The current temperature threshold
 */
int8_t get_temperature_threshold(void);

/**
 * \brief 
 * Set the temperature threshold.
 * 
 * \param temperature_threshold The temperature threshold to set
 */
void set_temperature_threshold(int8_t temperature_threshold);

#endif