# Arduino Control Unit

## Available serial commands
List of all the available serial commands. Each command will return the command name with a reponse in the following format: `<COMMAND_NAME>=<COMMAND_RESPONSE>`.

### PING
Check if the control unit is connected and responding.
#### Parameters
This command has no parameters.
#### Returns
The `PING` command returns `PONG`. So the full response to `PING` will be `PING=PONG`.
#### Example
`PING`

### INITIALIZE
Configure the Control Unit when it is not initialized. Without initialization the Control Unit cannot be used.
#### Parameters
The initialize command has 5 parameters that must be seperated by a comma.  
The first parameter is the control unit id, this is a 32bit unsigned decimal. The ID may not be `0`.  
The second parameter is the window height, the window height must be provided in cm and may not be more that 400cm.  
The third parameter is the temperature threshold in degrees celcius, this must be a value between -64 and +63.
The fourth parameter is the light intensity threshold as percentage, this must be a value between 0 and 100.
The fifth
#### Returns
The `INITIALIZE` command returns `OK` when the initialization was successful. `ERROR` will be returned when the unit is already initiliazed or invalid parameters have been provided.
#### Example
`INITIALIZE=4294967295,300,25,100,1`

### RESET
Reset the Control Unit.
#### Parameters
This command has no parameters.
#### Returns
The `RESET` command returns `OK`.
#### Example
`RESET`

### GET_ID
Get the Control Unit id.
#### Parameters
This command has no parameters.
#### Returns
The `GET_ID` returns a 32 bit unsigned decimal that represents the Control Unit id.
#### Example
`GET_ID`

### SET_ID
Set the Control Unit id.
#### Parameters
The id, a 32 bit unsinged decimal. The id may not be 0.
#### Returns
The `SET_ID` command returns `OK` when the id is set. When no or invalid parameters are provided `ERROR` will be returned.
#### Example
`SET_ID=4294967295`

### GET_WINDOW_HEIGHT
Get the window height.
#### Parameters
This command has no parameters.
#### Returns
The `GET_WINDOW_HEIGHT` returns the window height in cm with a maximum of 400cm.
#### Example
`GET_WINDOW_HEIGHT`

### SET_WINDOW_HEIGHT
Set the window height.
#### Parameters
The window height in cm, with a maximum value of 400cm.
#### Returns
The `SET_WINDOW_HEIGHT` command returns `OK` when the window height is set. When no or invalid parameters are provided `ERROR` will be returned.
#### Example
`SET_WINDOW_HEIGHT=300`

### GET_TEMP_THRESHOLD
Get the temperature threshold.
#### Parameters
This command has no parameters.
#### Returns
The `GET_TEMP_THRESHOLD` returns the temperature threshold as degrees celcius.
#### Example
`GET_TEMP_THRESHOLD`

### SET_TEMP_THRESHOLD
Set the temperature threshold.
#### Parameters
The temperature threshold as degrees celcius.
#### Returns
The `SET_TEMP_THRESHOLD` command returns `OK` when the temperature threshold is set. When no or invalid parameters are provided `ERROR` will be returned.
#### Example
`SET_TEMP_THRESHOLD=70`

### GET_LI_THRESHOLD
Get the light intensity threshold.
#### Parameters
This command has no parameters.
#### Returns
The `GET_LI_THRESHOLD` returns the light intensity threshold as a percentage.
#### Example
`GET_LI_THRESHOLD`

### SET_LI_THRESHOLD
Set the temperature threshold.
#### Parameters
The light intensity threshold as a percentage.
#### Returns
The `SET_LI_THRESHOLD` command returns `OK` when the light intensity threshold is set. When no or invalid parameters are provided `ERROR` will be returned.
#### Example
`SET_LI_THRESHOLD=70`

### GET_MANUAL
Get the manual control status.
#### Parameters
This command has no parameters.
#### Returns
The `GET_MANUAL` returns 1 when manual control is enabled and 0 when manual control is disabled.
#### Example
`GET_MANUAL`

### SET_MANUAL
Set the manual control mode.
#### Parameters
The manual control mode. When 1 is provided manual control will be enabled. When 0 is provided manual control will be disabled.
#### Returns
The `SET_MANUAL` command returns `OK` when the manual conrol is set. When no or invalid parameters are provided `ERROR` will be returned.
#### Example
`SET_MANUAL=1`

### GET_SENSOR_DATA
Get the sensor data.
#### Parameters
This command has no parameters.
#### Returns
The `GET_MANUAL` returns the temperature, light intensity and shutter status in the following format: `<TEMPERATURE>,<LIGHT_INTENSITY>,<SHUTTER_STATUS>`.  
The tempature is gived in degrees celcius.  
The light intensity is a percentage.  
The shutter status is a number: OPEN = 0, CLOSED = 1, OPENING = 2, CLOSING = 3.
#### Example
`GET_SENSOR_DATA`

### GET_SENSOR_HISTORY
Get the all collected sensor history and remove it from the Control Unit.
#### Parameters
This command has no parameters.
#### Returns
The `GET_MANUAL` will return 3 different things.  
First the history lenght will be returned in the following format: `L<HISTORY_SIZE>`.

Secondly the readings will be returned. This will be returned in chunks of 5 until the history size is reached. A reading is given in the following format `<TEMPERATURE>,<LIGHT_INTENSITY>,<SHUTTER_STATUS>`. All reading are separted by a `;`.

When all readings have been returned `OK` will be returned.
#### Example
`GET_SENSOR_HISTORY`

### ROLL_UP
Roll up the shutter.
#### Parameters
This command has no parameters.
#### Returns
The `ROLL_UP` command returns `OK` when everything is oke. When manual mode is disabled `ERROR` will be returned.

### ROLL_DOWN
Roll down the shutter.
#### Parameters
This command has no parameters.
#### Returns
The `ROLL_DOWN` command returns `OK` when everything is oke. When manual mode is disabled `ERROR` will be returned.