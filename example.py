# Import our PyElo library
import pyelo

# First, our Elo system is already setup with some default, commonly used values, but these
# optional functions can change them if desired:
pyelo.setMean(1000)
pyelo.setK(20)
pyelo.setRPA(400)
# Again, these above functions are optional. See wikipedia for how these variables might be changed in your program.
   
    
# Create two players for demonstration
adam = createPlayer("Adam")
bob = createPlayer("Bob")

# Lets add a chess game where Adam won, Bob lost, and no player had a home advantage
# Arguments: playerA,playerAScore,playerB,playerBScore,homeAdvA,homeAdvB,mov (margin of victory)
pyelo.addGameResults(adam,1,bob,0,0,0,0)

# Here are the results!
print("After Game 1, where Adam won, the Elo scores are now:")
print(pyelo.rankPlayers())
print("The odds of Adam beating Bob in another game are now:")
print(str(pyelo.getPlayerOdds(adam,bob))+"%")
    
