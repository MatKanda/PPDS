# Sync/Async
This branch is used for eighth week assignments where I'm working on simple
sync/async programs practicing couroutines.

Main goal was to create simple sync program and then refactor it into the async
one. Then observer changes, execution time etc.

I created simple card game where the **3** players are putting random cards
on the table and the player with the highest value wins. In sync form they
put cards on the table one by one, everyone has 2 seconds to put the card.
So the total time is minimum **6** seconds for code execution. In async form
they didn't wait for each other and all started at the same time.

Example output of sync code.
```
Peter is putting a card on the table.
Peter has put card '5' on the table.

Tomas is putting a card on the table.
Tomas has put card '8' on the table.

Ondrej is putting a card on the table.
Ondrej has put card '4' on the table.

The winner is Tomas with card '8'
```

Example output of async code.
```
Peter is putting a card on the table.
Tomas is putting a card on the table.
Ondrej is putting a card on the table.

Peter has put card '9' on the table.
Tomas has put card '10' on the table.
Ondrej has put card '9' on the table.

The winner is Tomas with card '10'
```
Interesting was to observe that when I wrote the code in wrong
order, e.g.
```
TABLE[seat] = CARDS[randint(0, N-1)]
await asyncio.sleep(2)
```
the program "knew" the cards before the were given on the table.
The output looked like this:
```
Peter is putting a card on the table.
Tomas is putting a card on the table.
Ondrej is putting a card on the table. 

The winner is Peter with card '9'

Peter has put card '9' on the table.
Tomas has put card '7' on the table.
Ondrej has put card '6' on the table.
```
So I needed to change the order so the execution is logically 
correct.
```
await asyncio.sleep(2)
TABLE[seat] = CARDS[randint(0, N-1)]
```
I solved the one problem and the second one appeared. The result
function was giving a result before the cards where put on the table.
```
Peter is putting a card on the table.
Tomas is putting a card on the table.
Ondrej is putting a card on the table.
It's a tie.
Peter has put card '7' on the table.
Tomas has put card '3' on the table.
Ondrej has put card '4' on the table.
```

This was caused because all three players were waiting so the last 
one ready was result function. I tried to solve this by adding
```Event()``` but it turned out that it is basically a blocking
call which cause kind of deadlock because the thread kept waiting
in the ```result()``` function and nothing could have continued.
Then I realised there is a simple solution. I simply removed function call
from ```gather()``` and called it after this part. and it worked perfectly.

The total time of code execution was down 3 times, from **6** to **2** seconds.
The reason is that the players wasn't waiting for each other to put cards but
everyone "started" putting their cards at the same time.

**License: MIT\
Author: Matúš Kanda\
School: Slovak University of Technology in Bratislava (STU)**

