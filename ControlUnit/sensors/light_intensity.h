#ifndef _SENSORS_LIGHT_SENSITIVITY_H_
#define _SENSORS_LIGHT_SENSITIVITY_H_

#include <stdint.h>

/**
 * \brief 
 * Get the current light intensity.
 * 
 * \return uint8_t Light intensity as a percentage.
 */
uint8_t get_light_intensity(void);

/**
 * \brief 
 * Check if the light intensity sensor is connected.
 * 
 * \return uint8_t unsigned 0 is sensor is not connected
 */
uint8_t light_intensity_sensor_connected(void);

#endif