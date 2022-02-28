# Semaphores & Events
This branch is used for second week assignments where I am working 
with synchronization using Semaphores and Events.

## Simple barrier
This task is in ```simple_barrier.py``` file. To achieve required 
behaviour I used ```Semaphores```. When this solution was working fine,
I switched to and ```Event```. The purpose was basically to execute 
some code **before** barrier, then create the point where all threads
will stop (barrier) and then release all the threads again to finish
the code **after**.

## Reusable barrier
This task is in ```reusable_barrier.py``` file. It was kind of
like "superstructure" of previous task. The purpose was to create 
reusable barrier which will be used in ```while``` loop. Once again,
I had **2** separate functions simulating some program code. They were
using ```print()``` to simulate some kind of output. In this task I
failed when I tried to use the same approach as in previous one.
It worked fine for the first iteration, but every other was not working
correctly. I decided to add another ```Barrier```. It did not help, so
I was wondering what can be wrong. Then I realised I'm using ```Event``` so
I have to user ```clear()``` method to reset ```Event``` settings. The 
position of this method was important as well. I had to clear it after
the barrier has done it's work, but before the next try.

## Fibonacci sequence
This task is in ```fibonacci.py``` file. The purpose of this task was
to compute Fibonacci sequence but every element of sequence will be
computed by separate thread. I had to create all the threads and then
release them all at once. I had to make sure that the threads will
compute at correct order because every **i+2** thread needs the 
previous **i** and **i+1** computation results. To be honest, my only
idea was to stop all the threads and then check the ```id``` of the thread that
entered the ```computation``` function.  Then **increment** counter 
which represents current acceptable thread and call the function recursively
again. You can choose between ```Semaphore``` and ```Event``` in the
initialization because u will create generic object ```Synchronization```
which can work with both.\
I used **1** ```mutex``` and **1**
```Synchronization``` object like ```Semaphore```
or ```Event``` inside my ```Class```.
I'm pretty sure that this is not ideal solution
and not even close as effective as it probably can be, but I didn't
come with anything better and this solution does the job.



**License: MIT\
Author: Matúš Kanda\
School: Slovak University of Technology in Bratislava (STU)**

