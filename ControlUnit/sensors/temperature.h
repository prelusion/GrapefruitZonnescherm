#ifndef _SENSORS_TEMPERATURE_H_
#define _SENSORS_TEMPERATURE_H_

/**
 * \brief 
 * Get the current temperature.
 * 
 * \return int8_t Signed number between -64 and +63
 */
int8_t get_temperature(void);

/**
 * \brief 
 * Check if the temperature sensor is connected.
 * 
 * \return uint8_t unsigned 0 is sensor is not connected
 */
uint8_t temperature_sensor_connected(void);

#endif