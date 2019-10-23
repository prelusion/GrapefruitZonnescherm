/**
 * \brief 
 * Get the current distance.
 * 
 * \return uint8_t unsigned number between 0 and 255
 */
uint8_t get_distance();

/**
 * \brief 
 * Check if the distance sensor is connected.
 * 
 * \return uint8_t unsigned 0 is sensor is not connected
 */
uint8_t distance_sensor_connected();