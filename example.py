"""
PyElo Library Example

This example demonstrates how to use the PyElo library to set up an Elo rating system,
create players, record game results, and rank players.

Author: Tony Cardillo
"""

from pyelo import (
    set_mean, set_K, set_RPA, set_home_adv_amount,
    create_player, add_game_results, rank_players, get_player_odds,
    WIN, LOSS, DRAW, HOME_ADVANTAGE, NO_HOME_ADVANTAGE, AWAY_ADVANTAGE
)

# Step 1: Set up the Elo system
set_mean(1000)                    # Set the starting Elo of all players
set_K(30)                         # Set the K-factor for rating adjustments
set_RPA(400)                      # Set the RPA (Rating Point Adjustment) value
set_home_adv_amount(50)           # Set the home advantage amount (additional points for the home team)

# Step 2: Create players
alice = create_player("Alice")
bob = create_player("Bob")
charlie = create_player("Charlie")

# Step 3: Record game results
# Alice plays Bob, Alice wins with a home advantage
add_game_results(alice, WIN, bob, LOSS, home_advantage=HOME_ADVANTAGE)

# Alice plays Charlie in a neutral game, and it's a draw
add_game_results(alice, DRAW, charlie, DRAW, home_advantage=NO_HOME_ADVANTAGE)

# Bob plays Charlie, Charlie wins with an away disadvantage
add_game_results(charlie, WIN, bob, LOSS, home_advantage=AWAY_ADVANTAGE)

# Step 4: Calculate the odds of Alice beating Bob
alice_vs_bob_odds = get_player_odds(alice, bob)
print(f"Odds of Alice beating Bob: {alice_vs_bob_odds:.2f}%")

# Step 5: Rank players by their current Elo ratings
ranked_players = rank_players()
print("Player Rankings:")
for player in ranked_players:
    print(player)

# Output:
# Odds of Alice beating Bob: 56.53%
# Player Rankings:
# Name: Alice (Elo: 1016.4)
# Name: Charlie (Elo: 1012.8)
# Name: Bob (Elo: 970.8)
