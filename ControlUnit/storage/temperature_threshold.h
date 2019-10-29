#ifndef _STORAGE_TEMPERATURE_THRESHOLD_H_
#define _STORAGE_TEMPERATURE_THRESHOLD_H_

/**
 * \brief 
 * Get the current temperature threshold.
 * 
 * \return uint8_t The current temperature threshold
 */
int16_t get_temperature_threshold(void);

/**
 * \brief 
 * Set the temperature threshold.
 * 
 * \param temperature_threshold The temperature threshold to set
 */
void set_temperature_threshold(int16_t temperature_threshold);

#endif