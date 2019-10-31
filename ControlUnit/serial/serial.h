#ifndef SERIAL_H_
#define SERIAL_H_

#include <avr/io.h>

void serial_init();
void serial_transmit(uint8_t data);
void serial_readln(char* buf, int maxlength);

#endif