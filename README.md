# Roller-coaster, Water molecule
This branch is used for sixth week assignments where I am working on Roller-coaster 
and Water molecule tasks.

# Roller-coaster
This task is in ```roller_coaster.py``` file. This task is  representing multiple 
trains giving a ride to multiple passengers. There can be only 1 train at the 
loading dock and 1 train at the unloading dock at the same time. Passengers are
boarding and unboarding the trains.\
The main purpose was to ensure, that only **1** train can load/unload the passengers at the
same time and to ensure that train will always wait for all passengers to board/unboard
before it moves away. There can't be for example 3 trains loading at the same time
or the train leaving while the passengers are still in process of boarding/unboarding.\
There are functions in the file simulating some actions like passenger boarding etc. which are 
printing some output to verify results and are set to sleep for given time.\
I'm using ```Semaphore``` and ```Barrier``` objects. The ```Barrier``` is little
modified, so the last thread which comes into the barrier and sets it free calls
```.signal()``` on the ```Semaphore``` passed as argument. This is used in ```passenger```
side of the code to signalize that all passengers are boarded/unboarded.

# Water molecule
This task is in ```water_molecule.py``` file. This task is  representing multiple 
```Threads``` trying to create molecule of water which consists of **2** hydrogen
atoms and **1** oxygen atom. The main idea is that the ```threads``` have to wait
for each other, so they have all the parts necessary to create a molecule.\
In this solution I'm using shared custom object ```Molecule``` that consists of
necessary objects and variables like ```Barrier```, ```Semaphore```, ```Mutex```
and counters for **oxygen** and **hydrogen**. In this case I'm using classic version
of ```Barrier```. The logic is pretty simple, the ```Threads``` are just going over
and over in while loop and waiting for the sufficient amount of atoms to build the
molecule. WHen it happens, the build it, decrement variables and do it over again.
We just have to be careful to place ```Mutex.unlock()``` in oxygen part of code, because if
we place it in hydrogen, there are more threads that can try to ```unlock``` already
unlocked lock and an error will occur.


**License: MIT\
Author: Matúš Kanda\
School: Slovak University of Technology in Bratislava (STU)**

