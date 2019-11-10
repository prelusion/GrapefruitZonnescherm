#ifndef _SCHEDULER_H_
#define _SCHEDULER_H_

#include <stdint.h>

// Scheduler data structure for storing task data
typedef struct
{
   // Pointer to task
   void (* task_function)(void);
   // Initial delay in ticks
   uint16_t delay;
   // Periodic interval in ticks
   uint16_t period;
   // Runme flag (indicating when the task is due to run)
   uint8_t run_me;
} TimerTask;

void timer_init(void);
void timer_start(void);
void timer_dispatch_tasks(void);
uint8_t timer_add_task(void (*)(void), const uint16_t, const uint16_t);
void timer_delete_task(const uint8_t);

#define timer_max_tasks (8)

#endif