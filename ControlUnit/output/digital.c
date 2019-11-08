#include "digital.h"

//serial includes
#include "../serial.h"

 #include <avr/io.h>
 #include <stdint.h>
 
 /*
 * Vcc : +5V, GND : ground
 * DIO : data (board pin 5)     (PD5)
 * CLK : clock (board pin 6)    (PD6)
 * STB : strobe (board pin 7) (PD7)
 */

#define HIGH 0x1
#define LOW  0x0

const uint8_t data = 5;
const uint8_t clock = 6;
const uint8_t strobe = 7;

/*0*/  /*1*/   /*2*/  /*3*/  /*4*/  /*5*/  /*6*/  /*7*/  /*8*/  /*9*/
const uint8_t digits[] = { 0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f };
	
/*T*/ /*E*/ /*M*/ /*P*/
const uint8_t temperature_display[] = { 0x78, 0x79, 0x15, 0x73 };
	
/*L*/  /*I*/   /* */  /* */
const uint8_t light_intesity_display[] = { 0x38, 0x30, 0x00, 0x00 };
	
/*D*/ /*I*/ /*S*/ /*T*/
const uint8_t distance_display[] = { 0x5e, 0x30, 0x6d, 0x78 };
	
uint8_t toggled_buttons;

// read value from pin
int read(uint8_t pin)
{
    if (PIND & _BV(pin)) { // if pin set in port
        return HIGH;
    } else {
        return LOW;
    }
}

// write value to pin
void write(uint8_t pin, uint8_t val)
{
    if (val == LOW) {
        PORTD &= ~(_BV(pin)); // clear bit
    } else {
        PORTD |= _BV(pin); // set bit
    }
}

// shift out value to data
void shift_out (uint8_t val)
{
    uint8_t i;
    for (i = 0; i < 8; i++)  {
        write(clock, LOW);   // bit valid on rising edge
        write(data, val & 1 ? HIGH : LOW); // lsb first
        val = val >> 1;
        write(clock, HIGH);
    }
}

// shift in value from data
uint8_t shift_in(void)
{
    uint8_t value = 0;
    uint8_t i;

    DDRD &= ~(_BV(data)); // clear bit, direction = input
    
    for (i = 0; i < 8; ++i) {
        write(clock, LOW);   // bit valid on rising edge
        value = value | (read(data) << i); // lsb first
        write(clock, HIGH);
    }
    
    DDRD |= _BV(data); // set bit, direction = output
    
    return value;
}

//Sends internal command to the digital display
void send_command(uint8_t value)
{
    write(strobe, LOW);
    shift_out(value);
    write(strobe, HIGH);
}

//Resets the display
void reset()
{
    // clear memory - all 16 addresses
    send_command(0x40); // set auto increment mode
    write(strobe, LOW);
    shift_out(0xc0);   // set starting address to 0
    for(uint8_t i = 0; i < 16; i++)
    {
        shift_out(0x00);
    }
    write(strobe, HIGH);
}

//Makes the ports valid for the display
void digital_setup()
{
    DDRD |= 0b11100000; // set pins 7,6,5 from port D as out put
    uint8_t buttons = 0;	
    send_command(0x89);  // activate and set brightness to medium
	reset();
}

//Gives a display on the led board of the selected measurement
void display_measurement(Sensor sensor, uint8_t measurement)
{
	reset();
    send_command(0x40); // auto-increment address
    write(strobe, LOW);
    shift_out(0xc0); // set starting address = 0
	
    for(uint8_t position = 0; position < 8; position++)
    {
		if (position < 4)
		{
			if(sensor == TEMPERATURE)
			{	
				shift_out(temperature_display[position]);
			}
			else if (sensor == LIGHT_INTENSITY)
			{
				shift_out(light_intesity_display[position]);
			} 
			else if (sensor == DISTANCE)
			{
				shift_out(distance_display[position]);
			}
		} 
		else if(position < 7)
		{
			if (position == 4)
			{
				uint8_t new_measurement = (measurement / 100);
				if (new_measurement == 0)
				{
					shift_out(0x00);
				}
				else
				{
					measurement -= new_measurement * 100;
					shift_out(digits[new_measurement]);
				}
			}
			else if(measurement < 100 && measurement >= 10 && position != 4)
			{
				uint8_t new_measurement = (measurement / 10);
				measurement -= new_measurement * 10;
				shift_out(digits[new_measurement]);	
			}
			else if(measurement >= 0 && measurement < 10 && position != 4)
			{
				shift_out(digits[measurement]);	
			}
			else if(measurement < 0 && position == 4 && sensor == TEMPERATURE)
			{
				shift_out(0xe3);
			}
		}
		else
		{
			if(sensor == TEMPERATURE)
			{
				shift_out(0xe3);
			}
			else if (sensor == LIGHT_INTENSITY)
			{
				shift_out(0x73);
			}
			else if (DISTANCE)
			{	
				shift_out(0x39);
			}
		}
        shift_out(0x00);
    }
    write(strobe, HIGH);
}

//Checks if new pressed button is valid
uint8_t check_new_pressed_buttons(void)
{
	uint8_t new_pressed_buttons = read_buttons();
	uint8_t buttons = get_toggled_buttons();
	if(new_pressed_buttons != buttons && new_pressed_buttons != 0x00)
	{
		buttons = new_pressed_buttons;
	}	
	return buttons;
}

//Reads all the digital buttons that are pressed
uint8_t read_buttons()
{
	uint8_t checked_buttons = 0;
	write(strobe, LOW);
	shift_out(0x42); // key scan (read buttons)

	DDRD &= ~(_BV(data)); // clear bit, direction = input

	for (uint8_t i = 0; i < 4; i++)
	{
		uint8_t v = shift_in() << i;
		checked_buttons |= v;
	}

	DDRD |= _BV(data); // set bit, direction = output
	write(strobe, HIGH);
	return (uint8_t)checked_buttons;

}

//Get the last pressed buttons
uint8_t get_toggled_buttons()
{
	return toggled_buttons;
}

//Set pressed button
void set_toggled_buttons(uint8_t new_toggled_buttons)
{
	toggled_buttons = new_toggled_buttons;
}