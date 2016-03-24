# Import the PyElo library
import pyelo

# Our Elo system is, by default, already setup with some default, commonly used values,
# but these optional functions can change them if desired:
pyelo.setMean(1000)
pyelo.setK(20)
pyelo.setRPA(400)
# Again, these above functions are optional. See wikipedia for how these variables might be changed in your program.
   
   
# Create two players for demonstration
adam = pyelo.createPlayer("Adam")
bob = pyelo.createPlayer("Bob")

# Lets add a chess game where Adam won, Bob lost, and no player had a home advantage
pyelo.addGameResults(adam, # playerA
                     1,    # playerAScore (1 = win in chess)
                     bob,  # playerB
                     0,    # playerBScore (0 = loss in chess)
                     0,    # homeAdvA (optional: 1 = home, -1 = away, 0 = neutral)
                     0,    # homeAdvB (optional, same flags as above)
                     0)    # mov (margin of victory, optional)

# Here are the results!
print("After Game 1, where Adam won, the Elo scores are now:")
print(pyelo.rankPlayers())
print("Thus, the odds of Adam beating Bob in another game are now:")
print(str(pyelo.getPlayerOdds(adam,bob))+"%")
    
