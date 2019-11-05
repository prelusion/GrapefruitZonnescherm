#ifndef SERIAL_H_
#define SERIAL_H_

#include <stdint.h>

/**
 * \brief 
 * Initialize the serial connection.
 */
void serial_init(void);

/**
 * \brief 
 * Transmit a character over serial.
 * 
 * \param data The ASCII character to transmit.
 */
void serial_transmit(uint8_t data);

#endif