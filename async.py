"""
Simple sync program used as base for next task where I will try to refactor it into the async code.

Imports "time, asyncio" and "random".

Author: Matúš Kanda
"""
import time
from random import randint
import asyncio


"""
Global variables.
    CARDS: cards the players can play with
    N: number of cards
    TABLE: array representing table with 3 seats
"""
CARDS = [2, 3, 4, 5, 6, 7, 8, 9, 10]
N = 9
TABLE = [0, 0, 0]


async def player(name, seat):
    """
    Function representing player picking a card and putting it on the table.

    Parameters
    ----------
    name: name of the player
    seat: his seat at the table

    :param name: name of the player
    :param seat: his seat at the table
    """
    global IS_CARDS
    print(f"{name} is putting a card on the table.")
    await asyncio.sleep(2)
    TABLE[seat] = CARDS[randint(0, N-1)]
    print(f"{name} has put card '{TABLE[seat]}' on the table.")


def result():
    """
    Function giving a winner of the game.
    """
    winner = None
    if TABLE[0] > TABLE[1] and TABLE[0] > TABLE[2]:
        winner = 0
    elif TABLE[1] > TABLE[0] and TABLE[1] > TABLE[2]:
        winner = 1
    elif TABLE[2] > TABLE[1] and TABLE[2] > TABLE[0]:
        winner = 2

    if winner is not None:
        if winner == 0:
            print(f"The winner is Peter with card '{TABLE[0]}'")
        if winner == 1:
            print(f"The winner is Tomas with card '{TABLE[1]}'")
        if winner == 2:
            print(f"The winner is Ondrej with card '{TABLE[2]}'")
    else:
        print("It's a tie.")


async def main():
    start_time = time.time()

    await asyncio.gather(player("Peter", 0), player("Tomas", 1), player("Ondrej", 2))
    result()

    print("\n--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    asyncio.run(main())
