# Nuclear Power & Philosophers
This branch is used for fourth week assignments where I am working on previous years
assignments. In this task I had to combine more synchronization ```Objects``` such as 
```Event()``` or ```Semaphore()```  and  synchronization ```methods``` like ```turnstile```
or ```Lightswitch```.\
\
My work here was to create the ```nuclear_power_two.py``` solution, because of our dear 
professor **Mr. Jokay** who showed us and explained first task ```nuclear_power_one.py```.
Because of that I'm going to concentrate on the **second** solution in this documentation
file. Those solutions ar similar, but it needed some adjustments which I'm going to explain
down below.\
\
I've done **Philosophers** task as well, where I had to create left/right-handed solution.

## Three sensors
In this case I had to create **three** sensors of **two** types. The first one is type 
**P** and **T**. This type of sensor needs **10-20ms** to update the data. The second type
is **H**. This sensor needs **20-25ms** to update the data. The sensors themselves update
the data every **50-60ms**.

## Monitors
I had to create **eight** monitors that will read the data written by sensors. Monitor's
data **update** time the takes **40-50ms**. The monitors are reading the data constantly
in ```while``` loop.

## Problems and solutions
Because the monitors are reading constantly in loop, and they hold the "room" all the time,
after the first run of **sensors** the never got back into the room (I've tested it) and 
sensor ```starvation``` happens. I had to refactor the ```barrier``` and```lightswitch```code 
in monitor's and sensor's ```functions```. The key was to create ```barrier``` 
outside of ```lightswitch``` lock in monitors and inside of ```lightswitch``` lock 
in sensors.\
I had to ensure that monitors start reading the data after they are written as well. In
this case I used an ```array``` of ```Event``` objects. Every ```index``` of the array
is representing one type of sensor. Every monitor is waiting to all **three** of them to
be set to ```signal()``` and starts the reading after that.

## Pseudocode
```    
def init():
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = [Event(), Event(), Event()]

    initialize 8 monitors

    initialize 3 types of sensors
    
def monitor(monitor_id, valid_data, turnstile, ls_monitor, access_data):

    wait for the every sensor to write the data before reading
    
    while True:
        turnstile.wait()
        turnstile.signal()
        reading_monitors = monitor's lightswitch lock
        read_time = random number from 40-50ms range 
        print(something that simalutes some output)
        sleep(read_time)
        monitor's lightswitch unlock


def sensor_p(sensor_id, turnstile, ls_sensor, valid_data, access_data):
    while True:
        sleep(random number from 50-60ms range)
        turnstile.wait()
        writing_sensors = sensor's lightswitch lock
        turnstile.signal()
        write_time = random number from 10-20ms range 
        print(something that simalutes some output)
        sleep(write_time)
        "signal()" for this sensor type
        sensor's lightswitch unlock
        
        
def sensor_h(sensor_id, turnstile, ls_sensor, valid_data, access_data):
   while True:
        sleep(random number from 50-60ms range)
        turnstile.wait()
        writing_sensors = sensor's lightswitch lock
        turnstile.signal()
        write_time = random number from 20-25ms range 
        print(something that simalutes some output)
        sleep(write_time)
        "signal()" for this sensor type
        sensor's lightswitch unlock

        
def sensor_t(sensor_id, turnstile, ls_sensor, valid_data, access_data):
    while True:
        sleep(random number from 50-60ms range)
        turnstile.wait()
        writing_sensors = sensor's lightswitch lock
        turnstile.signal()
        write_time = random number from 10-20ms range 
        print(something that simalutes some output)
        sleep(write_time)
        "signal()" for this sensor type
        sensor's lightswitch unlock
``` 

## Philosophers
The point of this task was to ensure that multiple philosophers can eat at the same time,
so I had to ensure that they pick the forks from the table only when the forks are available.
The forks is ```list``` of ```Semaphores``` where value **0** means fork is being used
and is not available and value **1** means fork is available on the table. I had to generate
random number representing number of left-handed philosophers. I decided to put it in
```<1,all-1>``` range. This means that there will be at least **1** left-handed philosopher
which is **crucial** for this sync problem solution. At the same time, ```all-1``` means
there won't be only left-handed philosophers, because then this **right/left-handed** solution
wouldn't make any sense. It would be the same situation as if there were only right-handed
philosophers.\
\
After the number generation I needed to add decision-making ```if/else``` into the
```put``` and ```get``` forks functions. It will decide which fork (left or right) will
get/put first and which one second, based on the ```hand``` parameter.

**License: MIT\
Author: Matúš Kanda\
School: Slovak University of Technology in Bratislava (STU)**

