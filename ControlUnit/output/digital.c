#include "digital.h"
#include <avr/io.h>
#include <stdio.h>

void show_temperature_digital(uint8_t temperature)
{
	show_measurement(TEMPERATURE, temperature);
}
 
void show_light_intensity_digital(uint8_t light_intensity)
{
	show_measurement(LIGHT_INTENSITY, light_intensity);
}
 
 /*
 * tm1638.c
 * bjab, march 2016
 * demo program interfacing TM1638 from Arduino UNO (ATmga238P)
 * reusing :
 *   -http://blog.3d-logic.com/2015/01/10/using-a-tm1638-based-board-with-arduino/
 *   -https://android.googlesource.com/platform/external/arduino/+/jb-mr1-dev/hardware/arduino/cores/arduino
 *
 * to keep things simple, we'll ony use PORTB
 *
 * Vcc : +5V, GND : ground
 * DIO : data (board pin 8)     (PD5)
 * CLK : clock (board pin 9)    (PD6)
 * STB : strobe (board pin 10) (PD7)
 *
 */

#include <avr/io.h>
#include <stdint.h>
#include <util/delay.h>

#define HIGH 0x1
#define LOW  0x0

const uint8_t data = 5;
const uint8_t clock = 6;
const uint8_t strobe = 7;

uint8_t counting(void); // need to put them in .h

// read value from pin
int read(uint8_t pin)
{
    if (PINB & _BV(pin)) { // if pin set in port
        return HIGH;
    } else {
        return LOW;
    }
}

// write value to pin
void write(uint8_t pin, uint8_t val)
{
    if (val == LOW) {
        PORTB &= ~(_BV(pin)); // clear bit
    } else {
        PORTB |= _BV(pin); // set bit
    }
}

// shift out value to data
void shiftOut (uint8_t val)
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
uint8_t shiftIn(void)
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

void sendCommand(uint8_t value)
{
    write(strobe, LOW);
    shiftOut(value);
    write(strobe, HIGH);
}

void reset()
{
    // clear memory - all 16 addresses
    sendCommand(0x40); // set auto increment mode
    write(strobe, LOW);
    shiftOut(0xc0);   // set starting address to 0
    for(uint8_t i = 0; i < 16; i++)
    {
        shiftOut(0x00);
    }
    write(strobe, HIGH);
}

void setup()
{
     DDRB=0xff; // set port B as out put

    sendCommand(0x89);  // activate and set brightness to medium
//  reset();
}

uint8_t show_measurement(Sensor sensor, uint8_t measurement)
{
	/*0*/  /*1*/   /*2*/  /*3*/  /*4*/  /*5*/  /*6*/  /*7*/  /*8*/  /*9*/
	uint8_t digits[] = { 0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f };
	switch(sensor)
	{
		case TEMPERATURE:
			/*T*/ /*E*/ /*M*/ /*P*/
			uint8_t letters[] = { 0xf0, 0xf2, 0x2a, 0xce};
		break;
		case LIGHT_INTENSITY:
	
			/*L*/  /*I*/
			uint8_t letters[] = { 0x70, 0x60, 0x00, 0x00 };
		break;
	}

    sendCommand(0x40); // auto-increment address
    write(strobe, LOW);
    shiftOut(0xc0); // set starting address = 0
    for(uint8_t position = 0; position < 8; position++)
    {
		if (position < 4)
		{
			shiftOut(letters[position])
		} 
		else if(position < 7)
		{
			if(measurement < 100 && measurement >= 0)
			{
				shiftOut();
			}
			else if(measurement < 0 && position == 4 && sensor == TEMPERATURE)
			{
				shiftOut(0x80);
			}
			else
			{
				shiftOut(0xfe);
			}
		}
		else
		{
			if(sensor == TEMPERATURE)
			{
				shiftOut(0xc6);
			}
			else
			{
				shiftOut(0xb8);
			}
		}
        shiftOut(digits[digit]);
        _delay_ms(100);
        shiftOut(0x00);
    }

    write(strobe, HIGH);

    //return (digit == 0);
}