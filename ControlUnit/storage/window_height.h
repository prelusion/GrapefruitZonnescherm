#ifndef _STORAGE_WINDOW_HEIGHT_H_
#define _STORAGE_WINDOW_HEIGHT_H_

#include <stdint.h>

/**
 * \brief 
 * Get the window height.
 * 
 * \return uint16_t The window hight in CM
 */
uint16_t get_window_height(void);

/**
 * \brief 
 * Set the window height.
 * 
 * \param window_height The window height to set in CM
 */
void set_window_height(uint16_t window_height);

#endif