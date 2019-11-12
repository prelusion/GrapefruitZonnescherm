#include "digital.h"

//serial includes
#include "../serial.h"

#include <avr/io.h>
#include <string.h>
#include <stdio.h>

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

/*0*/  /*1*/   /*2*/  /*3*/  /*4*/  /*5*/  /*6*/  /*7*/  /*8*/  /*9*/ /* C */ /*D*/ /* E */ /* I */ /* L */ /* M */ /* P */ /* S */ /* T */ /* G */ /*   */
const uint8_t characters[] = { 0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x39, 0x5e, 0x79, 0x30, 0x38, 0x15, 0x73, 0x6d, 0x78, 0xe3, 0x00 };

// read_pin_from_display value from pin
int read_pin_from_display(uint8_t pin)
{
	if (PIND & _BV(pin)) { // if pin set in port
		return HIGH;
		} else {
		return LOW;
	}
}

// write_pin_from_display value to pin
void write_pin_from_display(uint8_t pin, uint8_t val)
{
	if (val == LOW) {
		PORTD &= ~(_BV(pin)); // clear bit
		} else {
		PORTD |= _BV(pin); // set bit
	}
}

// shift out value to data
void write_value_to_display (uint8_t val)
{
	uint8_t i;
	for (i = 0; i < 8; i++)  {
		write_pin_from_display(clock, LOW);   // bit valid on rising edge
		write_pin_from_display(data, val & 1 ? HIGH : LOW); // lsb first
		val = val >> 1;
		write_pin_from_display(clock, HIGH);
	}
}

// shift in value from data
uint8_t read_settings_from_display(void)
{
	uint8_t value = 0;
	DDRD &= ~(_BV(data)); // clear bit, direction = input
	
	for (uint8_t i = 0; i < 8; ++i) {
		write_pin_from_display(clock, LOW);   // bit valid on rising edge
		value = value | (read_pin_from_display(data) << i); // lsb first
		write_pin_from_display(clock, HIGH);
	}
	
	DDRD |= _BV(data); // set bit, direction = output
	
	return value;
}

//Sends internal command to the digital display
void send_command_to_display(uint8_t value)
{
	write_pin_from_display(strobe, LOW);
	write_value_to_display(value);
	write_pin_from_display(strobe, HIGH);
}

//Resets the display
void reset_display()
{
	// clear memory - all 16 addresses
	send_command_to_display(0x40); // set auto increment mode
	write_pin_from_display(strobe, LOW);
	write_value_to_display(0xc0);   // set starting address to 0
	for(uint8_t i = 0; i < 16; i++)
	{
		write_value_to_display(0x00);
	}
	write_pin_from_display(strobe, HIGH);
}

//Makes the ports valid for the display
void init_digital_display()
{
	DDRD |= 0b11100000; // set pins 7,6,5 from port D as out put
	send_command_to_display(0x89);  // activate and set brightness to medium
	reset_display();
}

//Gives a display on the led board of the selected measurement
void display_measurement(SelectedSensor sensor, int16_t measurement)
{
	reset_display();
	send_command_to_display(0x40); // auto-increment address
	write_pin_from_display(strobe, LOW);
	write_value_to_display(0xc0); // set starting address = 0
	
	char text[5];
	char unit;
	char value[8];
	switch (sensor)
	{
		case TEMPERATURE:
		strcpy(text, "TEMP");
		unit = 'G';
		sprintf(value, "%s%3d%c", text, (uint8_t)measurement, unit);
		break;
		case LIGHT_INTENSITY:
		strcpy(text, "LI  ");
		unit = 'P';
		sprintf(value, "%s%3d%c", text, (uint8_t)measurement, unit);
		break;
		case DISTANCE:
		strcpy(text, "DIST");
		unit = 'C';
		sprintf(value, "%s%3d%c", text, measurement, unit);
		break;
	}
	
	
	for(uint8_t position = 0; position < 8; position++)
	{
		uint8_t character_index;
		
		switch (value[position])
		{
			case '0':
			character_index = 0;
			break;
			case '1':
			character_index = 1;
			break;
			case '2':
			character_index = 2;
			break;
			case '3':
			character_index = 3;
			break;
			case '4':
			character_index = 4;
			break;
			case '5':
			character_index = 5;
			break;
			case '6':
			character_index = 6;
			break;
			case '7':
			character_index = 7;
			break;
			case '8':
			character_index = 8;
			break;
			case '9':
			character_index = 9;
			break;
			case 'C':
			character_index = 10;
			break;
			case 'D':
			character_index = 11;
			break;
			case 'E':
			character_index = 12;
			break;
			case 'I':
			character_index = 13;
			break;
			case 'L':
			character_index = 14;
			break;
			case 'M':
			character_index = 15;
			break;
			case 'P':
			character_index = 16;
			break;
			case 'S':
			character_index = 17;
			break;
			case 'T':
			character_index = 18;
			break;
			case 'G':
			character_index = 19;
			break;
			default:
			character_index = 20;
		}
		
		write_value_to_display(characters[character_index]);
		write_value_to_display(0x00);
	}
	write_pin_from_display(strobe, HIGH);
}

//Checks if new pressed button is valid
uint8_t check_new_pressed_buttons_from_display(void)
{
	uint8_t new_pressed_buttons = read_pressed_display_buttons();
	uint8_t buttons = get_current_selected_buttons();
	if(new_pressed_buttons != buttons && new_pressed_buttons != 0x00)
	{
		buttons = new_pressed_buttons;
	}
	return buttons;
}

//read_pin_from_displays all the digital buttons that are pressed
uint8_t read_pressed_display_buttons()
{
	uint8_t checked_buttons = 0;
	write_pin_from_display(strobe, LOW);
	write_value_to_display(0x42); // key scan (read_pin_from_display buttons)

	DDRD &= ~(_BV(data)); // clear bit, direction = input

	for (uint8_t i = 0; i < 4; i++)
	{
		uint8_t v = read_settings_from_display() << i;
		checked_buttons |= v;
	}

	DDRD |= _BV(data); // set bit, direction = output
	write_pin_from_display(strobe, HIGH);
	return (uint8_t)checked_buttons;

}