#ifndef _STORAGE_MANUAL_H_
#define _STORAGE_MANUAL_H_

#include <stdint.h>
#include <avr/io.h>

/**
 * \brief 
 * Get the manual status.
 * 
 * \return uint8_t The manual status, 0 if not manual
 */
uint8_t get_manual(void);

/**
 * \brief
 * Set the manual status.
 * 
 * \param manual The manual status to set.
 */
void set_manual(uint8_t manual);

#endif