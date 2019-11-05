#include <avr/io.h>
#include "../data.h"

//Sets the shutter
void init_shutter_status(void)
{
	//TODO initialize the right shutter status at the start of the control unit
	set_current_shutter_status(CLOSED);
}

//Checks if the shutter reached its status destination and returns it. Returns the same status if its not yet reached
ShutterStatus check_shutter_reached_endpoint(ShutterStatus status, uint16_t distance, uint16_t window_height)
{
	if(status == OPEN || status == CLOSED) 
	{
		return status;
	}
	if(status == CLOSING)
	{
		if(distance < 10)
		{
			return CLOSED;
		}
	}
	else
	{
		if(distance >= window_height)
		{
			return OPEN;
		}
	}
	return status;
}