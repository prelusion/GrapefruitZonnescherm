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
 
/** 
 * \brief  
 * Checks if the next shutter status should be open or closed.
 * After checks set the right shutter status and update leds.  
 *
 * Void no returns 
 */
void update_shutter_status(void);

/** 
 * \brief  
 * Checks every minute if the shutter should change checking the temperature and light intensity
 *  
 * Void no returns 
 */
void check_shutter_status(void);