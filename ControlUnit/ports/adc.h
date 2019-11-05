#ifndef _PORTS_ADC_H_
#define _PORTS_ADC_H_

#include <stdint.h>

/**
 * \brief 
 * Sets the ADC port and gives it a frequency so a prescaler.
 */
void adc_init(void);

/**
 * \brief 
 * Read the value of the provided analog channel.
 * 
 * \param adc_channel The channel to read.
 * 
 * \return uint16_t The analog value.
 */
uint16_t adc_read(uint8_t adc_channel);

#endif