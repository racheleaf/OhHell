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

	def get_card(self):
		if self.cards:
			return self.cards.pop()
		return None

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
		self.cards = {
			"C": [],
			"D": [],
			"H": [],
			"S": [],
		}

	def reset(self):
		for suit in ["C", "D", "H", "S"]:
			self.cards[suit] = []

	def get_all_cards(self):
		all_cards = []
		for suit, cards in self.cards.items():
			all_cards += cards
		return all_cards

	def draw(self, card):
		self.cards[card.suit].append(card)

	def get_suit_order(self, suit, trump_suit): 
		suits = ["C", "D", "H", "S"]
		suit_order = [suit]
		suits.remove(suit)
		if (suit != trump_suit):
			suit_order.append(trump_suit)
			suits.remove(trump_suit)
		suit_order += suits
		return suit_order

	def play(self, suit, trump_suit):
		suit_order = self.get_suit_order(suit, trump_suit)
		for s in suit_order:
			if self.cards[s]:
				return self.cards[s].pop()
		return None

	def lead(self):
		suits = ["C", "D", "H", "S"]
		random.shuffle(suits)
		card = None
		while len(suits):
			suit = random.choice(suits)
			suits.remove(suit)
			if (self.cards[suit]):
				return self.cards[suit].pop()

			







