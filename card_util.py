import random

class Card: 

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.face_up = False

class Deck:

	def __init__(self, suits, ranks):
		self.cards = []
		for suit in suits:
			for rank in ranks:
				self.cards.append(Card(suit, rank))

	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self, hands, numCards, dealer): 
		i = dealer
		cardsSoFar = 0
		while len(self.cards) > 0:
			if i % len(hands) == dealer:
				cardsSoFar += 1
				if cardsSoFar == numCards + 1:
					break
			card = self.cards.pop()
			hands[i % len(hands)].draw(card)
			i += 1

class Hand:

	def __init__(self):
		self.cards = []

	def draw(self, card):
		self.cards.append(card)




