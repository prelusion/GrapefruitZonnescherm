#ifndef SERIAL_H_
#define SERIAL_H_

#include <stdint.h>

void serial_init(void);
void serial_transmit(uint8_t data);
void serial_readln(uint8_t* buffer, uint16_t max_length);

#endif