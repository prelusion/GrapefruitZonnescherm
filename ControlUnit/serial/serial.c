#include <avr/io.h>
#include <stdio.h>
#include "serial.h"

// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51

// Putchar tbv. stdio.h
// bron: https://www.nongnu.org/avr-libc/user-manual/group__avr__stdio.html
static int ser_stdio_putchar(char c, FILE *stream) {
	if (c=='\n') {
		ser_transmit('\r');
	}
	ser_transmit(c);
	return 0;
}

void secret_msg() {
	printf("Hallo jan wytze");
}

static FILE uart_output = FDEV_SETUP_STREAM(ser_stdio_putchar, NULL, _FDEV_SETUP_WRITE);

void ser_init() {
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable TX and RX
	UCSR0B = _BV(TXEN0) | _BV(RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
	// Setup stdout
	stdout=&uart_output;
}

// Low level transmit
void ser_transmit(uint8_t data) {
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

