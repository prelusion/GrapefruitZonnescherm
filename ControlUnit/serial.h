#ifndef SERIAL_H_
#define SERIAL_H_

#include <stdint.h>

void serial_init(void);
void serial_transmit(uint8_t data);

#endif