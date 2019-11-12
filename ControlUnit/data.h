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

typedef enum {
	TEMPERATURE = 0,
	LIGHT_INTENSITY = 1,
	DISTANCE = 2
} SelectedSensor;

/**
 * \brief 
 * Check if serial is connected.
 * 
 * \return uint8_t returns 0 when serial is not connected.
 */
uint8_t get_current_serial_connection(void);

/**
 * \brief 
 * Set the serial connection status.
 * 
 * \param serial_connected 0 when serial is not connected.
 */
void set_current_serial_connection(uint8_t serial_connected);

/**
 * \brief 
 * Get the last measured temperature.
 * 
 * \return int8_t The temperature in degrees Celcius.
 */
int8_t get_current_temperature(void);


/**
 * \brief 
 * Set the last measured temperature.
 * 
 * \param temperature The temperature in degrees Celcius.
 */
void set_current_temperature(int8_t temperature);

/**
 * \brief 
 * Get the last measured light intensity.
 * 
 * \return uint8_t The light intensity as a percentage.
 */
uint8_t	get_current_light_intensity(void);


/**
 * \brief 
 * Set the last measured light intensity. 
 * 
 * \param light_intensity The light intensity as a percentage
 * 
 * \return void
 */
void set_current_light_intensity(uint8_t light_intensity);

/**
 * \brief 
 * Get the current shutter status.
 * 
 * \return ShutterStatus The current shutter status.
 */
ShutterStatus get_current_shutter_status(void);
/**
 * \brief 
 * Set the current shutter status.
 * 
 * \param shutter_status The shutter status to set.
 */
void set_current_shutter_status(ShutterStatus shutter_status);

/**
 * \brief 
 * Get the current unit status.
 *
 * \return UnitStatus The current unit status.
 */
UnitStatus get_current_unit_status(void);

/**
 * \brief 
 * Set the current unit status.
 * 
 * \param unit_status The unit status to set.
 */
void set_current_unit_status(UnitStatus unit_status);

/**
 * \brief 
 * Get the selected sensor
 * 
 * \returns the selected sensor
 */
 SelectedSensor get_current_selected_sensor();
 
/** 
 * \brief  
 * Set the current selected sensor.
 *
 *\param selected_sensor The sensor to select.
 */

 void set_current_selected_sensor(SelectedSensor selected_sensor);
 
#endif