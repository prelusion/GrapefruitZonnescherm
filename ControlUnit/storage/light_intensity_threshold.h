#ifndef _STORAGE_LIGHT_INTENSITY_H_
#define _STORAGE_LIGHT_INTENSITY_H_

/**
 * \brief 
 * Get the current light intensity threshold.
 * 
 * \return uint8_t The current light intensity threshold
 */
uint8_t get_light_intensity_threshold(void);

/**
 * \brief 
 * Set the light intensity threshold.
 * 
 * \param light_intensity_threshold The light intensity threshold to set
 */
void set_light_intensity_threshold(uint8_t light_intensity_threshold);

#endif