'''
PyElo Library for easy implementation of Elo systems.
View the README for documentation, and check out example.py to see a common chess example.

@author: Tony Cardillo, cardilloab@gmail.com

Function List:

def setMean(mean)  
def setK(K)
def setRPA(RPA)
def getPlayerOdds(teamA,teamB)
def createPlayer(handle)
def rankPlayers()   
def addGameResults(teamA,teamAScore,teamB,teamBScore,homeAdvA,homeAdvB,mov)
'''

# Import math functionality, used for exponentiation
import math

# The Elo class contains the underlying variables for the Elo algorithm
class Elo:
    def __init__(self,mean,k,RPA):
        self.mean = 1000
        self.K = 20
        self.RPA = 400
        self.homeAdvAmt = None
        
    def addGame(self,teamA,teamAScore,teamB,teamBScore,homeAdvA,homeAdvB,mov):
        ''' 
            homeAdv = a flag that indicates if home advantage is a factor. 1 = home game; -1 = away game; 0 = neutral location
                Use the function setHomeAdv() to set the amount of additional points expected at a home game 
            mov = Margin of Victory, a flag that indicates if you want to factor in HOW much the winner won by. 1 = yes; 0 = no
                In chess, this would be 0. Sports like basketball and football may want to use a value of 1.
        '''      
        # Add a game to both teams total number of games
        teamA.numGames = teamA.numGames + 1
        teamB.numGames = teamB.numGames + 1

        # Determine win/losses
        scoreDif = teamAScore - teamBScore
        if scoreDif > 0:
            win = 1 # Win is form the perspective of team A by convention
            teamA.wins = teamA.wins + 1
            teamB.losses = teamB.losses + 1
            
            # If you had the lower Elo but still won...you created an upset.
            if teamA.elo < teamB.elo:
                teamA.upsets = teamA.upsets + 1
                teamB.beenUpset = teamB.beenUpset + 1
        elif scoreDif < 0:
            win = 0
            teamA.losses = teamA.losses + 1
            teamB.wins = teamB.wins + 1
            
            # If you had the higher Elo but still lost...you've been upset.
            if teamA.elo > teamB.elo:
                teamA.beenUpset = teamA.beenUpset + 1
                teamB.upsets = teamB.upsets + 1
        else:
            win = 0.5
            teamA.draws = teamA.draws + 1
            teamB.draws = teamB.draws + 1
            # For now, no upset counting on draws
                              
        # Calculate new Elo for A
        if homeAdvA == 1:
            # You are expected to do better if home, and thus the difference between you is less
            expectedScore = 1.0 / (1.0 + math.pow(10.0,(teamB.elo-teamA.elo-eloSystem.homeAdvAmt)/eloSystem.RPA))
        elif homeAdvA == -1:
            # Your opponent is expected to do better if you are away, and thus the difference between you is greater
            expectedScore = 1.0 / (1.0 + math.pow(10.0,(teamB.elo-teamA.elo+eloSystem.homeAdvAmt)/eloSystem.RPA))
        else:
            # Neutral site, no bonuses to anyone
            expectedScore = 1.0 / (1.0 + math.pow(10.0,(teamB.elo-teamA.elo)/eloSystem.RPA))
            
        # Calculate new Elo for B
        if homeAdvB == 1:
            # You are expected to do better if home, and thus the difference between you is less
            expectedScore = 1.0 / (1.0 + math.pow(10.0,(teamA.elo-teamB.elo-eloSystem.homeAdvAmt)/eloSystem.RPA))
        elif homeAdvB == -1:
            # Your opponent is expected to do better if you are away, and thus the difference between you is greater
            expectedScore = 1.0 / (1.0 + math.pow(10.0,(teamA.elo-teamB.elo+eloSystem.homeAdvAmt)/eloSystem.RPA))
        else:
            # Neutral site, no bonuses to anyone
            expectedScore = 1.0 / (1.0 + math.pow(10.0,(teamA.elo-teamB.elo)/eloSystem.RPA))
        
            
        # Positive if you win, negative if you lose.
        # More positive if you were less likely to win (an upset)
        # More positive if you had a higher margin of victory (scoreDif)
        if mov > 0:
            teamA.elo = teamA.elo + eloSystem.K*(win - expectedScore)*math.log(abs(scoreDif)+1)
            teamB.elo = teamB.elo + eloSystem.K*((1-win) - expectedScore)*math.log(abs(scoreDif)+1)
        else:
            teamA.elo = teamA.elo + eloSystem.K*(win - expectedScore)
            teamB.elo = teamB.elo + eloSystem.K*((1-win) - expectedScore)

# Setup our default Elo system with some commonly used values
eloSystem = Elo(1000,20,400)

# The Player class contains generic data about the player's Elo rating, wins/losses, and even upsets
# Not all of these variables must be used, but they are kept track of automatically anyway
class Player:
    def __init__(self, name):
        self.name = name
        self.numGames = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.elo = eloSystem.mean
        self.upsets = 0
        self.beenUpset = 0
        
    def __repr__(self):
        return "Name:  "+self.name+"("+str(self.elo)+")"
    
    def __str__(self):
        return "Name:  "+self.name+"("+str(self.elo)+")"
        
    def reset(self):
        self.numGames = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.elo = eloSystem.mean
        self.upsets = 0
        self.beenUpset = 0

playerList = []

def setMean(mean):
    ''' returns: None
    This sets the starting Elo of all future players, and represents what the average player will be ranked.
    If you reset a player, it will also reset to this value. By default, this value is 1000.
    ''' 
    eloSystem.mean = mean
    
    
def setK(K):
    ''' returns: None
    This sets the K-factor used to determine how dynamic the Elo system is at responding to change. High values lead to larger
    fluctuations that may over-respond, and small values lead to small fluctuations that may lack sensitivity. 
    In chess, K ranges anywhere from 10 to 40, depending on the rating organization and professional status of the players.
    By default, this value is 20.
    '''
    eloSystem.K = K
    
    
def setRPA(RPA):
    ''' returns: None
    The RPA, set to 400 in most systems, represents the difference in Elo ratings between 2 players that will result in the
    higher-rated player winning 10 times as often. Thus, with an RPA of 400, a match between an 1800 and 1400 player will
    result in the 1800 player winning 10 times more often. By default, this value is 400.
    '''
    eloSystem.RPA = RPA
    
    
def createPlayer(handle):
    ''' returns: a class Player() 
    handle is the reference to a player or team you want to start ranking. It may be a string of the player's name, for example.
    The new player is automatically added to playerList, a list of all players that may be sorted.
    '''
    newPlayer = Player(handle)
    playerList.append(newPlayer)
    return newPlayer
     
     
def rankPlayers():     
    ''' returns: a descending sorted list of all the players currently ranked in your Elo system. 
    '''
    return sorted(playerList, key=lambda player: player.elo, reverse=True) 


def getPlayerOdds(teamA,teamB):
    ''' returns: a float from 0.0 to 100.0 that represents the percentage odds that teamA will beat teamB 
    '''
    return 100.0 / (1.0 + math.pow(10.0,(teamB.elo-teamA.elo)/eloSystem.RPA))   


def addGameResults(teamA,teamAScore,teamB,teamBScore,homeAdvA=0,homeAdvB=0,mov=0):
    ''' returns: None
        teamA is the class returned from createPlayer()
        teamAScore is the score of team A. In chess, a win is 1, a loss is 0, and a draw is 0.5.
        teamB and teamBScore are the same format as teamA.
        homeAdvA is an optional flag for whether teamA has a home advantage. 1 means a home game, -1 means an away game, and 0 is a neutral location (default).
        homeAdvB is an optional flag for teamB's home advantage and follows the same format as above.
        mov stands for Margin of Victory, and is an optional flag for whether to take into account the size of the victory. 1 means yes, 0 means no (default).
            You would use 0 for chess, and probably 1 for games such as basketball, football/soccer, etc.
    '''
    eloSystem.addGame(teamA,teamAScore,teamB,teamBScore,homeAdvA,homeAdvB,mov)
    
    
def setHomeAdvAmt(homeAdvAmt):
    ''' returns: None
        This sets the amount, in Elo points, that a home-advantage team is expected to have.
        In chess, there is no well known home team advantage. 
        For other sports, set homeAdvAmt equal to your K-factor (default: 20) times the number of game points advantage.
            In basketball, this might be 60 Elo (20 * 3 baskets = 60 Elo)
            This is an inexact science, so results may vary.
    '''
    eloSystem.homeAdvAmt = homeAdvAmt
    
