#ifndef DATA_H_
#define DATA_H_

#include <avr/io.h>

typedef enum {
	OPEN = 0,
	CLOSED = 1,
	OPENING = 2,
	CLOSING = 3
} ShutterStatus;

int8_t get_current_temperature(void);
void set_current_temperature(int8_t temperature);

uint8_t	get_current_light_intensity(void);
void set_current_light_intensity(uint8_t light_intensity);

uint16_t get_current_distance(void);
void set_current_distance(uint16_t distance);

ShutterStatus get_current_shutter_status(void);
void set_current_shutter_status(ShutterStatus shutter_status);

#endif