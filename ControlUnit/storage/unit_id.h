/**
 * \brief 
 * Get the current unit id.
 * 
 * \return uint8_t The current unit id, 0 if no unit id is set
 */
uint16_t get_unit_id();

/**
 * \brief
 * Set the unit id.
 * 
 * \param unit_id The unit id to set
 */
void set_unit_id(uint16_t unit_id);

/**
 * \brief 
 * Check if the unit id is set.
 * 
 * \return uint8_t 0 when no unit id is set
 */
uint8_t has_unit_id();