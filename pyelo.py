# PyElo Library for easy implementation of Elo systems.
# View the README for documentation, and check out example.py to see a common chess example.
# @author: Tony Cardillo, cardilloab@gmail.com

# Import math functionality, used for exponentiation
import math
from typing import List

# Constants
WIN = 1
LOSS = 0
DRAW = 0.5
NO_HOME_ADVANTAGE = 0
HOME_ADVANTAGE = 1
AWAY_ADVANTAGE = -1

class Elo:
    def __init__(self, mean: int = 1000, k: int = 20, RPA: int = 400) -> None:
        self.mean = mean
        self.K = k
        self.RPA = RPA
        self.home_advantage = 0

    def set_home_adv(self, home_adv: int) -> None:
        self.home_advantage = home_adv

    def add_game(self, teamA, teamAScore: float, teamB, teamBScore: float, home_advantage: int = NO_HOME_ADVANTAGE, mov: int = 0) -> None:
        teamA.numGames += 1
        teamB.numGames += 1

        scoreDif = teamAScore - teamBScore
        if scoreDif > 0:
            win = 1  # Team A wins
            teamA.wins += 1
            teamB.losses += 1

            if teamA.elo < teamB.elo:
                teamA.upsets += 1
                teamB.beenUpset += 1
        elif scoreDif < 0:
            win = 0  # Team B wins
            teamA.losses += 1
            teamB.wins += 1

            if teamA.elo > teamB.elo:
                teamA.beenUpset += 1
                teamB.upsets += 1
        else:
            win = 0.5  # Draw
            teamA.draws += 1
            teamB.draws += 1

        # Calculate expected scores with home advantage for both teams
        expectedScoreA = self._calculate_expected_score(teamA.elo, teamB.elo, home_advantage)
        expectedScoreB = self._calculate_expected_score(teamB.elo, teamA.elo, -home_advantage)  # Invert the advantage for the opponent

        if mov > 0:
            teamA.elo += self.K * (win - expectedScoreA) * math.log(abs(scoreDif) + 1)
            teamB.elo += self.K * ((1 - win) - expectedScoreB) * math.log(abs(scoreDif) + 1)
        else:
            teamA.elo += self.K * (win - expectedScoreA)
            teamB.elo += self.K * ((1 - win) - expectedScoreB)


    def _calculate_expected_score(self, eloA: float, eloB: float, homeAdv: int) -> float:
        adjustment = self.home_advantage if homeAdv == HOME_ADVANTAGE else -self.home_advantage if homeAdv == AWAY_ADVANTAGE else 0
        return 1.0 / (1.0 + math.pow(10.0, (eloB - eloA + adjustment) / self.RPA))


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.numGames = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.elo = eloSystem.mean
        self.upsets = 0
        self.beenUpset = 0

    def __repr__(self) -> str:
        return f"Name: {self.name} ({self.elo})"

    def reset(self) -> None:
        self.numGames = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.elo = eloSystem.mean
        self.upsets = 0
        self.beenUpset = 0


playerList: List[Player] = []

# Elo system setup
eloSystem = Elo()

def set_mean(mean: int) -> None:
    eloSystem.mean = mean

def set_K(K: int) -> None:
    eloSystem.K = K

def set_RPA(RPA: int) -> None:
    eloSystem.RPA = RPA

def set_home_adv_amount(home_advantage: int) -> None:
    eloSystem.set_home_adv(home_advantage)

def create_player(handle: str) -> Player:
    newPlayer = Player(handle)
    playerList.append(newPlayer)
    return newPlayer

def rank_players() -> List[Player]:
    return sorted(playerList, key=lambda player: player.elo, reverse=True)

def get_player_odds(teamA: Player, teamB: Player) -> float:
    return 100.0 / (1.0 + math.pow(10.0, (teamB.elo - teamA.elo) / eloSystem.RPA))

def add_game_results(teamA: Player, teamAScore: float, teamB: Player, teamBScore: float, home_advantage: int = 0, mov: int = 0) -> None:
    eloSystem.add_game(teamA, teamAScore, teamB, teamBScore, home_advantage, mov)
