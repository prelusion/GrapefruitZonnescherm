/**
 * \brief 
 * Get the current light sensitivity.
 * 
 * \return uint8_t Unsigned number between 0 and 255
 */
uint8_t get_light_sensitivity();

/**
 * \brief 
 * Check if the light sensitivity sensor is connected.
 * 
 * \return uint8_t unsigned 0 is sensor is not connected
 */
uint8_t light_sensitivity_sensor_connected();