#include "scheduler.h"
#include <avr/interrupt.h>

// The array of tasks
TimerTask timer_tasks[timer_max_tasks];

void timer_dispatch_tasks(void)
{
   // Dispatches (runs) the next task (if one is ready)
   for (uint8_t index = 0; index < timer_max_tasks; index++)
   {
      if (timer_tasks[index].run_me > 0 && timer_tasks[index].task_function)
      {
         (*timer_tasks[index].task_function)();  // Run the task
         timer_tasks[index].run_me -= 1;   // Reset / reduce RunMe flag

         // Periodic tasks will automatically run again
         // - if this is a 'one shot' task, remove it from the array
         if (!timer_tasks[index].period)
         {
            timer_delete_task(index);
         }
      }
   }
}

uint8_t timer_add_task(void (*function)(), const uint16_t delay, const uint16_t period)
{
   uint8_t index = 0;

   // First find a gap in the array (if there is one)
   while ((timer_tasks[index].task_function != 0) && (index < timer_max_tasks))
   {
      index++;
   }

   // Have we reached the end of the list?   
   if (index == timer_max_tasks)
   {
      // Task list is full, return an error code
      return timer_max_tasks;  
   }

   // If we're here, there is a space in the task array
   timer_tasks[index].task_function = function;
   timer_tasks[index].delay = delay;
   timer_tasks[index].period = period;
   timer_tasks[index].run_me = 0;

   // return position of task (to allow later deletion)
   return index;
}

void timer_delete_task(const uint8_t TASK_INDEX)
{
   timer_tasks[TASK_INDEX].task_function = 0;
   timer_tasks[TASK_INDEX].delay = 0;
   timer_tasks[TASK_INDEX].period = 0;
   timer_tasks[TASK_INDEX].run_me = 0;
}

void timer_init(void)
{
   for (uint8_t i = 0; i < timer_max_tasks; i++)
   {
      timer_delete_task(i);
   }

   // Set up Timer 2
   // Values for 1ms and 10ms ticks are provided for various crystals
   OCR2A = (uint16_t)156;   		     // ~10ms = (1024/16.000.000) * 156
   TCCR2B = (1 << CS20) | (1 << CS21) | (1 << CS22) | (1 << WGM22);  // prescale op 1024, top counter = value OCR2A (CTC mode)
   TIMSK2 = 1 << OCIE2A;   		     // Timer 2 Output Compare A Match Interrupt Enable
}

void timer_start(void)
{
      sei();
}

ISR(TIMER2_COMPA_vect)
{
   for (uint8_t index = 0; index < timer_max_tasks; index++)
   {
      // Check if there is a task at this location
      if (timer_tasks[index].task_function)
      {
         if (timer_tasks[index].delay == 0)
         {
            // The task is due to run, Inc. the 'RunMe' flag
            timer_tasks[index].run_me += 1;

            if (timer_tasks[index].period)
            {
               // Schedule periodic tasks to run again
               timer_tasks[index].delay = timer_tasks[index].period;
               timer_tasks[index].delay -= 1;
            }
         }
         else
         {
            // Not yet ready to run: just decrement the delay
            timer_tasks[index].delay -= 1;
         }
      }
   }
}