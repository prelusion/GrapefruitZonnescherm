#include <avr/io.h>
#include <stdio.h>

#include "scheduler.h"
#include "data.h"

//status includes
#include "status/shutter.h"
#include "status/output.h"

//serial includes
#include "serial.h"

//ports includes
#include "ports/adc.h"

// Sensor includes
#include "sensors/distance.h"
#include "sensors/light_intensity.h"
#include "sensors/temperature.h"

// Storage includes
#include "storage/unit_id.h"
#include "storage/history.h"
#include "storage/temperature_threshold.h"
#include "storage/light_intensity_threshold.h"
#include "storage/window_height.h"

//Task index of added shutter tasks
 uint8_t shutter_task_index;

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
	uint16_t measurement = (current_temperature << 9) | ((current_light_intensity / 2) << 2) | current_shutter_status;
	
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

void update_shutter_status(void)
{
	uint16_t distance = get_distance();
	uint16_t window_height = get_window_height();
	ShutterStatus current_shutter_status = get_current_shutter_status();
	//Updates the new shutter status
	ShutterStatus new_shutter_status = check_shutter_reached_endpoint(current_shutter_status, distance, window_height);
	//If the shutter status is open of closed. Remove the task and change the leds
	if(new_shutter_status == OPEN || new_shutter_status == CLOSED)
	{	
		timer_delete_task(shutter_task_index);
		current_shutter_status = new_shutter_status;
		set_current_shutter_status(current_shutter_status);
	}
	control_leds(current_shutter_status);
}


void check_thresholds(void)
{
	int8_t current_temperature = get_current_temperature();
	uint8_t current_light_intensity = get_current_light_intensity();
	ShutterStatus current_shutter_status = get_current_shutter_status();
	//Check if the shutter has to close or open
	if (current_temperature > get_temperature_threshold() || current_light_intensity > get_light_intensity_threshold())
	{
		if(current_shutter_status != CLOSED)
		{
			//Set shutter status to closing
			set_current_shutter_status(CLOSING);
		}
	} else {
		if(current_shutter_status != OPEN)
		{
			//Set shutter status to opening
			set_current_shutter_status(OPENING);
		}
	}
	control_leds(current_shutter_status);
	//if the shutter status is opening or closing add a task;
	if (current_shutter_status == OPENING || current_shutter_status == CLOSING)
	{
		shutter_task_index = timer_add_task(&update_shutter_status, (uint16_t)0, (uint16_t)50); // 40 * 10ms = .5sec
	}
}

int main(void)
{
	adc_init();
	init_history();
	output_ports();
	serial_init();
	init_distance_sensor();
	init_shutter_status();
	
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
	
	init_distance_sensor();
	timer_add_task(&update_temperature, (uint16_t)0, (uint16_t)4000); // 4000 * 10ms = 40sec
	timer_add_task(&update_light_intensity, (uint16_t)0, (uint16_t)3000); // 3000 * 10ms = 30sec
	timer_add_task(&update_history, (uint16_t)200, (uint16_t)6000); // 6000 * 10ms = 60sec
	timer_add_task(&check_thresholds, (uint16_t)10, (uint16_t)1000); // 6000 * 10ms = 60sec
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
