#include "shutter.h"
#include <avr/io.h>
#include "../scheduler.h"

//status includes
#include "output.h"

// Sensor includes
#include "../sensors/distance.h"
#include "../sensors/light_intensity.h"
#include "../sensors/temperature.h"

// Storage includes
#include "../storage/temperature_threshold.h"
#include "../storage/light_intensity_threshold.h"
#include "../storage/window_height.h"


//Sets the shutter
void init_shutter_status(void)
{
	//TODO initialize the right shutter status at the start of the control unit
	set_current_shutter_status(CLOSED);
}

//Checks if the shutter reached its status destination and returns it. Returns the same status if its not yet reached
ShutterStatus check_shutter_reached_endpoint(ShutterStatus status, uint16_t distance, uint16_t window_height)
{
	if(status == CLOSING && distance < 10)
	{
		return CLOSED;
	}
	if(status == OPENING && distance >= window_height)
	{
		return OPEN;
	}
	return status;
}

uint8_t shutter_task_index;
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

void check_shutter_status(void)
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
	}
	else 
	{
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