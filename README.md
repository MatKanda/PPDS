# Smokers and Savages
This branch is used for fifth week assignments where I am working
on ```Smokers``` and ```Savages``` tasks.

# Smokers
This task is in ```smokers.py``` file. It represents **smokers** 
making their cigarettes and waiting for resources to be able to
make them. The **agents** are providing the resources and **pushers**
are managing delivered resources either on the table or to the smokers.

There is a **prioritization** problem. If there are many resources
available, the smokers eventually don't have to wait. But there
is an ```if - elif - else``` which involuntarily forces to
give priority to the first ```if``` statement. I decided to
solve this by adding another ```if``` at the beginning. Firstly
I will find out if there are both resources available, e.g. paper
and tobacco and if so, I will generate random number from **0-1**
interval which decides which of the resource will be passed.

# Savages
This solution is in ```savages.py``` file. My assignment was
to edit existing solution by creating possibility to add more
cooks. I've tried a few solutions. Firstly, I needed to create
multiple threads representing multiple cooks. Then I wanted them
to cook separately, so I added loop in range of total required
servings. Every loop added **1** serving into the pot. I added
one more barrier for cooks, because I wanted them to start cooking
at the same time. By output ```print``` I could see that they all
arrived at the barrier but only the last one arrived did the cooking.
I tried to add **turnstile** to the cooking process, but it didn't help.
Possible reason that came up to my mind is once again fifo front problem.
But there can be problem with barrier as well, because I could observe
that once the pot needed to be cooked again, the previous waiting cook
did the cooking. This might mean that they are waiting in front.
But what confuses me is that the barrier is outside the function call
(```line 218```) so all the threads should be released at once and
all of them should go into the function call on the line ```222```.
I added separate mutex for cooks so multiple threads doesn't increment
```serving``` variable at the same time more times than required.

## Pseudocode of edited functions
```
def put_servings_in_pot(m, cook_id, shared):
for loop:
    mutex.lock()
    print(some kind of output)
    # cooking the meal
    sleep()
    shared.servings += 1
    mutex.unlock()
    

def cook(m, cook_id, shared):
    shared.cook_barrier.wait()
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(m, cook_id, shared)
        shared.full_pot.signal()
```

**License: MIT\
Author: Matúš Kanda\
School: Slovak University of Technology in Bratislava (STU)**

