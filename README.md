# Thread assignment
This branch is used for first week assignments where I am working 
with threads.\
Every solution is in separate file. I've been using locks from
```threading``` module.

## First solution
This solution is in ``` solution_one.py``` file.\
In this solution I placed lock in the lines ```19``` and ```25```. First one is 
lock and second one is release the lock. The locks are placed inside
the while which causes the threads to switch from one to another.
One thread uses the lock, does the inside of the while and then release.
After that, another thread can take the control and does the same thing.

## Second solution
This solution is in ```solution_two.py``` file.\
In this solution I placed lock in lines ```18``` and ```25```. In this case I locked
the whole while loop, meaning that only the one thread will do all 
the work. One thread will lock, then iterate through the whole array
and then release.

## Third solution
This solution is in ```solution_three``` .py file.\
This solution does basically the same thing as the second one, but the
position of lock is different. This time it's placed in lines 
```29``` and ```31```meaning it locks before the first function 
call and then release 
after that.


**Author: Matúš Kanda\
License: MIT\
School: Slovak University of Technology in Bratislava (STU)**

