/** 
 * \brief  
 * Initializes the shutter status at startup 
 *  
 * Void no returns 
 */ 
void init_shutter_status(void); 
 
/** 
* \brief 
* Checks if the task should end the opening or closed shutter status 
* 
* Returns a ShutterStatus 
*/ 
ShutterStatus check_shutter_reached_endpoint(ShutterStatus status, uint16_t distance, uint16_t window_height); 