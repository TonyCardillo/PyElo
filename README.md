# PyElo
PyElo is a simple Python library for creating Elo ranking systems within your programs. Use it for chess, basketball, football, or any other head-to-head sport you can think of! Simply import pyelo into your existing software, and start ranking.

Below is a quick example, from example.py, that shows how PyElo can model the results of a chess game:
(see example.py for a fully commented version)

import pyelo

adam = pyelo.createPlayer("Adam")
bob = pyelo.createPlayer("Bob")

pyelo.addGameResults(adam,1,bob,0)

print("After Game 1, where Adam won, the Elo scores are now:")
print(pyelo.rankPlayers())
print("Thus, the odds of Adam beating Bob in another game are now:")
print(str(pyelo.getPlayerOdds(adam,bob))+"%")
    
