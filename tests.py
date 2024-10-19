import unittest
from pyelo import *

class TestPyElo(unittest.TestCase):
    
    def setUp(self):
        # Create some players with default Elo system setup
        self.player1 = create_player("Alice")
        self.player2 = create_player("Bob")
        set_mean(1000)
        set_K(30)
        set_RPA(400)
        set_home_adv_amount(50)

    def test_create_player(self):
        self.assertEqual(self.player1.name, "Alice")
        self.assertEqual(self.player1.elo, 1000)

    def test_rank_players(self):
        self.player1.elo = 1200
        self.player2.elo = 1100
        ranked_players = rank_players()
        self.assertEqual(ranked_players[0].name, "Alice")

    def test_add_game_results(self):
        add_game_results(teamA = self.player1, teamAScore=1, 
                         teamB = self.player2, teamBScore=0, 
                         mov=0)
        self.assertGreater(self.player1.elo, 1000)
        self.assertLess(self.player2.elo, 1000)

    def test_get_player_odds(self):
        odds = get_player_odds(self.player1, self.player2)
        self.assertIsInstance(odds, float)
        self.assertGreater(odds, 0)
        self.assertLess(odds, 100)

    def test_home_advantage(self):
        # Without home advantage
        add_game_results(self.player1, 1, self.player2, 0, home_advantage=0)
        no_home_elo_A = self.player1.elo
        no_home_elo_B = self.player2.elo
        
        # Reset Elo for next test
        self.player1.reset()
        self.player2.reset()

        # With home advantage for player 1
        add_game_results(self.player1, 1, self.player2, 0, home_advantage=1)
        home_adv_elo_A = self.player1.elo
        home_adv_elo_B = self.player2.elo

        # Print Elo values for debugging
        print(f"No Home Advantage - Player A: {no_home_elo_A}, Player B: {no_home_elo_B}")
        print(f"With Home Advantage - Player A: {home_adv_elo_A}, Player B: {home_adv_elo_B}")

        # Assert that home advantage made a difference
        self.assertNotEqual(no_home_elo_A, home_adv_elo_A, "Home advantage should impact Elo changes for player A")
        self.assertNotEqual(no_home_elo_B, home_adv_elo_B, "Home advantage should impact Elo changes for player B")

        self.assertNotEqual(no_home_elo_B, home_adv_elo_B, "Home advantage should impact Elo changes")

    def test_margin_of_victory(self):
        initial_elo_A = self.player1.elo
        initial_elo_B = self.player2.elo

        # Without margin of victory consideration
        add_game_results(self.player1, 3, self.player2, 0, mov=0)
        no_mov_elo_A = self.player1.elo
        no_mov_elo_B = self.player2.elo

        # Reset Elo for next test
        self.player1.elo = initial_elo_A
        self.player2.elo = initial_elo_B

        # With margin of victory consideration
        add_game_results(self.player1, 3, self.player2, 0, mov=1)
        mov_elo_A = self.player1.elo
        mov_elo_B = self.player2.elo

        # Check that the Elo changes are different with and without margin of victory
        self.assertNotEqual(no_mov_elo_A, mov_elo_A, "Margin of victory should impact Elo changes")
        self.assertNotEqual(no_mov_elo_B, mov_elo_B, "Margin of victory should impact Elo changes")
    
    def test_correct_elo_update(self):
        self.player1.elo = 1400
        self.player2.elo = 1200
        expected_elo_A_after = 1400 + 30 * (1 - (1 / (1 + math.pow(10, (1200 - 1400) / 400))))
        expected_elo_B_after = 1200 + 30 * (0 - (1 / (1 + math.pow(10, (1400 - 1200) / 400))))

        add_game_results(self.player1, 1, self.player2, 0, mov=0)

        self.assertAlmostEqual(self.player1.elo, expected_elo_A_after, places=1)
        self.assertAlmostEqual(self.player2.elo, expected_elo_B_after, places=1)

    def test_draw_results(self):
        self.player1.elo = 1300
        self.player2.elo = 1300
        add_game_results(self.player1, 0.5, self.player2, 0.5, mov=0)

        # Since both players have the same Elo and drew, there should be no change
        self.assertAlmostEqual(self.player1.elo, 1300, places=1)
        self.assertAlmostEqual(self.player2.elo, 1300, places=1)

    def test_upset_win(self):
        self.player1.elo = 1000
        self.player2.elo = 1500

        # Calculate expected Elo change for upset win (lower-rated player wins)
        expected_elo_A_after = 1000 + 30 * (1 - (1 / (1 + math.pow(10, (1500 - 1000) / 400))))
        expected_elo_B_after = 1500 + 30 * (0 - (1 / (1 + math.pow(10, (1000 - 1500) / 400))))

        add_game_results(self.player1, 1, self.player2, 0, mov=0)

        self.assertGreater(self.player1.elo, expected_elo_A_after - 1)
        self.assertLess(self.player2.elo, expected_elo_B_after + 1)

if __name__ == "__main__":
    unittest.main(failfast=True)
