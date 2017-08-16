import card_util

class Game:

	def __init__(self, num_players):
		suits = ("C", "D", "H", "S")
		ranks = range(1, 14)
		self.round = 1
		self.dealer = 0
		self.you = 0
		self.deck = card_util.Deck(suits, ranks)
		self.deck.shuffle()
		self.hands = []
		for i in range(num_players):
			self.hands.append(card_util.Hand())

	def deal(self):
		self.deck.deal(self.hands, 4, self.dealer)


