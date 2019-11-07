#include "shutter.h"
#include <avr/io.h>
#include "../scheduler.h"

//output includes
#include "status.h"

// Sensor includes
#include "../sensors/distance.h"
#include "../sensors/light_intensity.h"
#include "../sensors/temperature.h"

// Storage includes
#include "../storage/window_height.h"

// The scheduler index of the task that controls the shutter.
uint8_t shutter_task_index;

//Sets the shutter
void init_shutter_status(void)
{
	//TODO initialize the right shutter status at the start of the control unit, maybe use EEPROM to store the current shutterstatus so it will be available at start?
	set_current_shutter_status(CLOSED);
	update_leds();
}

void control_shutter(void)
{
	uint16_t distance = get_distance();
	uint16_t window_height = get_window_height();
	ShutterStatus current_shutter_status = get_current_shutter_status();
	
	if (current_shutter_status == CLOSING && distance < 10)
	{
		set_current_shutter_status(CLOSED);
		timer_delete_task(shutter_task_index);
	}
	
	if (current_shutter_status == OPENING && distance >= window_height)
	{
		set_current_shutter_status(OPEN);
		timer_delete_task(shutter_task_index);
	}
	
	update_leds();
}

void shutter_roll_up(void)
{
	ShutterStatus current_shutter_status = get_current_shutter_status();
	
	// Check if the shutter is already open or is opening.
	if (current_shutter_status == OPEN || current_shutter_status == OPENING)
	{
		return;
	}
	
	// Check if the shutter is closing.
	if (current_shutter_status == CLOSING)
	{
		// Cancel the closing of the shutter.
		timer_delete_task(shutter_task_index);
	}
	
	set_current_shutter_status(OPENING);
	shutter_task_index = timer_add_task(&control_shutter, (uint16_t)0, (uint16_t)50); // 50 * 10ms = .5sec
}

void shutter_roll_down(void)
{
	ShutterStatus current_shutter_status = get_current_shutter_status();
	
	// Check if the shutter is already closed or is closing.
	if (current_shutter_status == CLOSED || current_shutter_status == CLOSING)
	{
		return;
	}
	
	// Check if the shutter is opening.
	if (current_shutter_status == OPENING)
	{
		// Cancel the opening of the shutter.
		timer_delete_task(shutter_task_index);
	}
	
	set_current_shutter_status(CLOSING);
	shutter_task_index = timer_add_task(&control_shutter, (uint16_t)0, (uint16_t)50); // 50 * 10ms = .5sec
}