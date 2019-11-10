#include <avr/io.h>
#include <stdio.h>

#include "scheduler.h"
#include "data.h"

//serial includes
#include "serial.h"

//status includes
#include "output/shutter.h"
#include "output/status.h"

//ports includes
#include "ports/adc.h"

// Sensor includes
#include "sensors/distance.h"
#include "sensors/light_intensity.h"
#include "sensors/temperature.h"

// Storage includes
#include "storage/unit_id.h"
#include "storage/history.h"
#include "storage/manual.h"
#include "storage/temperature_threshold.h"
#include "storage/light_intensity_threshold.h"
#include "storage/window_height.h"


void update_history(void)
{
	// Check if the unit is connected to the control center.
	if (!get_current_serial_connection())
	{
		// When connected there is no need to keep the history.
		return;
	}
	
	int8_t current_temperature = get_current_temperature();
	uint8_t current_light_intensity = get_current_light_intensity();
	ShutterStatus current_shutter_status = get_current_shutter_status();
	
	// 16 bit per measurement:
	//   0  0  0  0  0  0  0     0  0  0  0  0  0  0     0  0
	// |      Temperature     |    Light intensity    | Shutter status
	uint16_t measurement = (current_temperature << 9) | (current_light_intensity << 2) | current_shutter_status;
	
	write_measurement(measurement);
}

/**
 * \brief 
 * Update the temperature in the current_unit_statistics struct.
 */
void update_temperature(void)
{
	set_current_temperature(get_temperature());
}

/**
 * \brief 
 * Update the light intensity in the current_unit_statistics struct.
 */	
void update_light_intensity(void)
{
	set_current_light_intensity(get_light_intensity());
}

/**
 * \brief 
 * Check if the shutter has to be opened or closed based on the temperature and light intensity.
 */	
void check_thresholds(void)
{
	if (get_manual())
	{
		return;
	}
	
	if (get_current_temperature() > get_temperature_threshold() || get_current_light_intensity() > get_light_intensity_threshold())
	{
		shutter_roll_down();
	}
	else
	{
		shutter_roll_up();
	}
}

/**
 * \brief 
 * Receive the last known shutter status from EEPROM and set it.
 */	
void initialize_shutter(void)
{
	init_shutter_status();
}

int main(void)
{
	adc_init();
	init_history();
	serial_init();
	init_distance_sensor();
	init_leds();
	
	if (!has_unit_id())
	{
		set_current_unit_status(INITIALIZING);
	}
	
	#ifndef DISABLE_SENSOR_CHECK
	// Check if all sensors are connected.
	if (!(distance_sensor_connected() && light_intensity_sensor_connected() && temperature_sensor_connected()))
	{
		// TODO show the error with blinking LEDs.
		// TODO maybe save which sensor is not connected.
		set_current_unit_status(SENSOR_ERROR);
	}
	#endif
		
	// Initialize the timer.
	timer_init();

	timer_add_task(&update_temperature, (uint16_t)0, (uint16_t)4000); // 4000 * 10ms = 40sec
	timer_add_task(&update_light_intensity, (uint16_t)0, (uint16_t)3000); // 3000 * 10ms = 30sec
	timer_add_task(&update_history, (uint16_t)200, (uint16_t)6000); // 6000 * 10ms = 60sec
	timer_add_task(&check_thresholds, (uint16_t)10, (uint16_t)6000); // 6000 * 10ms = 60sec
	//Initializes the status as a task because the  timer has to be initialized before this works.
	timer_add_task(&initialize_shutter, (uint16_t)0, (uint16_t)0);
	timer_start();
	
	if (get_current_unit_status() == STARTING)
	{
		// Initializating and sensor check passed, serial communication is ready and scheduler is ready.
		set_current_unit_status(OPERATING);
	}
	
    while (1) 
    {
		timer_dispatch_tasks();
    }
}
