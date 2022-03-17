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

**License: MIT\
Author: Matúš Kanda\
School: Slovak University of Technology in Bratislava (STU)**

