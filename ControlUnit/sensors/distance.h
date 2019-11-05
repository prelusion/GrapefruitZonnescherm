#ifndef _SENSORS_DISTANCE_H_
#define _SENSORS_DISTANCE_H_

#include <stdint.h>

void init_distance_sensor(void);

/**
 * \brief 
 * Get the current distance.
 * 
 * \return uint16_t Distance in CM.
 */
uint16_t get_distance(void);

/**
 * \brief 
 * Check if the distance sensor is connected.
 * 
 * \return uint8_t 0 if sensor is not connected
 */
uint8_t distance_sensor_connected(void);

#endif