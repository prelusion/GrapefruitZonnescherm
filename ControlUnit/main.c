#include <avr/io.h>


//serial includes
#include "serial/serial.h"
//ports includes
#include "ports/adc.h"
#include "ports/ports.h"

// Sensor includes
#include "sensors/distance.h"
#include "sensors/light_intensity.h"
#include "sensors/temperature.h"

// Storage includes
#include "storage/unit_id.h"

// Enum that indicates the unit status.
enum unit_status{STARTING, OPERATING, INITIALIZING, ERROR} control_unit_status = STARTING;

struct ControlUnitConfiguration {
	uint16_t	unit_id;
	uint8_t		window_height;
	int8_t		temperature_threshold;
	uint8_t		light_intensity_threshold;
} control_unit_configuration;

struct ControlUnitData {
	int8_t		temperature;
	uint8_t		light_intensity;
	uint8_t		distance;
	uint8_t		screen_status;
} control_unit_data;

/**
 * \brief 
 * Update the temperature in the current_unit_statistics struct.	
 */
void update_temperature()
{
	control_unit_data.temperature = get_temperature();
}

/**
 * \brief 
 * Update the light sensitivity in the current_unit_statistics struct.
 */	
void update_light_sensitivity()
{
	control_unit_data.light_intensity = get_light_intensity();
}

/**
 * \brief 
 * Update the distance in the current_unit_statistics struct.
 */	
void update_distance()
{
	control_unit_data.distance = get_distance();
}

int main(void)
{
	init_ports();
	adc_init();
	ser_init();
	if (!has_unit_id()) {
		// TODO don't operate but listen for initialisation.
		control_unit_status = INITIALIZING;
		return 1;
	}
	
	// Check if all sensors are connected.
	if (!(distance_sensor_connected() && light_intensity_sensor_connected() && temperature_sensor_connected()))
	{
		// TODO show the error with blinking LEDs.
		// TODO maybe save which sensor is not connected.
		control_unit_status = ERROR;
		return 1;
	}
	
	// Load the configuration into RAM for quick access.
	control_unit_configuration.unit_id = get_unit_id();
	control_unit_configuration.window_height = get_window_height();
	control_unit_configuration.temperature_threshold = get_temperature_threshold();
	control_unit_configuration.light_intensity_threshold = get_light_intensity_threshold();
	
	// TODO execute sensor updates by timer scheduling.
	
	// TODO handle serial communication, maybe do this in the infinite loop.
	
	// Initializating and sensor check passed, serial communication is ready and scheduler is running.
	control_unit_status = OPERATING;
	uint8_t init_data;
    while (1) 
	{
		
	}
}
