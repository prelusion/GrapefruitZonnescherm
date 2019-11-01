#ifndef _STORAGE_HISTORY_H_
#define _STORAGE_HISTORY_H_

#include <stdint.h>

typedef struct {
	uint16_t	size; // The data size.
	uint16_t*	data; // Pointer to data.
} History;

/**
 * \brief 
 * Initialize the history storage.
 */
void init_history(void);

/**
 * \brief 
 * Get all saved history.
 * 
 * \return History
 */
History load_history(void);


/**
 * \brief 
 * Clear all stored history.
 */
void clear_history(void);

/**
 * \brief 
 * Write a measurement to the history.
 *
 * \param value
 */
void write_measurement(uint16_t value);

#endif