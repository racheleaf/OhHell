import game_util
from functools import reduce
import helpers

print("Welcome to this sketchy Python implementation of the card game Oh Hell.")
num_players_str = input("Enter a number of players (2-10): ").strip()
num_players = 0
while True:
	if helpers.check_int(num_players_str):
		num_players = int(num_players_str)
		if num_players >= 2 and num_players <= 10:
			break
		if num_players < 2:
			num_players_str = input("There should be at least 2 players. Enter a number of players: ")
		else:
			num_players_str = input("More than 10 players is not recommended. Enter a different number of players: ")
	else:
		num_players_str = input("Enter a valid number of players: ")

game = game_util.Game(num_players)
game.play()

