import game_util

game = game_util.Game(5)
game.deal()

for hand in game.hands:
	print(len(hand.cards))
