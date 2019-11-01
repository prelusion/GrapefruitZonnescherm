#ifndef DATA_H_
#define DATA_H_

#include <stdint.h>

typedef enum {
	OPEN = 0,
	CLOSED = 1,
	OPENING = 2,
	CLOSING = 3
} ShutterStatus;

// Enum that indicates the unit status.
typedef enum {
	STARTING = 0, // The unit is starting.
	OPERATING = 1, // Everything is OK!
	INITIALIZING = 2, // The unit is not initialized, the unit first has to be initialized before it can be used, most commands will not work.
	SENSOR_ERROR = 3 // Not all sensors are connected.
} UnitStatus;

int8_t get_current_temperature(void);
void set_current_temperature(int8_t temperature);

uint8_t	get_current_light_intensity(void);
void set_current_light_intensity(uint8_t light_intensity);

uint16_t get_current_distance(void);
void set_current_distance(uint16_t distance);

ShutterStatus get_current_shutter_status(void);
void set_current_shutter_status(ShutterStatus shutter_status);

UnitStatus get_current_unit_status(void);
void set_current_unit_status(UnitStatus unit_status);

#endif