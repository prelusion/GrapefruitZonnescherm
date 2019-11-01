#include <avr/io.h>
#include <stdio.h>

#include "scheduler.h"
#include "data.h"

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
#include "storage/history.h"

#include "command_processing.h"

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
 * Update the distance in the current_unit_statistics struct.
 */	
void update_distance(void)
{
	set_current_distance(get_distance());
}

void process_serial(void)
{
	char buffer[255];
	serial_readln(buffer, sizeof(buffer));
	
	process_input(buffer);
}

int main(void)
{
	init_ports();
	adc_init();
	serial_init();
	
	// Set unit status to starting.
	set_current_unit_status(STARTING);
	
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
	timer_add_task(&process_serial, (uint16_t)0, (uint16_t)2); // 2 * 10ms = 20ms
	//TODO task update_distance wordt nog niet uigevoerd.
	timer_add_task(&update_distance, (uint16_t)0, (uint16_t)2000); // 2000 * 10ms = 20sec
	timer_add_task(&update_temperature, (uint16_t)0, (uint16_t)4000); // 4000 * 10ms = 40sec
	timer_add_task(&update_light_intensity, (uint16_t)0, (uint16_t)3000); // 3000 * 10ms = 30sec
	timer_start();
	
	// TODO handle serial communication, maybe do this in the infinite loop.
	
	// Initializating and sensor check passed, serial communication is ready and scheduler is ready.
	set_current_unit_status(OPERATING);
	
    while (1) 
    {
		timer_dispatch_tasks();
    }
}
