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

	def __init__(self, isYou):
		self.cards = {
			"C": [],
			"D": [],
			"H": [],
			"S": [],
		}
		self.isYou = isYou

	def reset(self):
		for suit in ["C", "D", "H", "S"]:
			self.cards[suit] = []

	def get_all_cards(self):
		all_cards = []
		for suit, cards in self.cards.items():
			all_cards += cards
		return all_cards

	def print_all_cards(self):
		all_cards = self.get_all_cards()
		print("ALL YOUR CARDS:")
		for card in all_cards:
			print(card.suit, card.rank)

	def get_you_card_choice(self):
		card_chosen = None
		while True:
			card_str = input("Pick a card to play: ")
			card_info = card_str.split(" ")
			if len(card_info) == 2:
				suit = card_info[0]
				if suit in ["C", "D", "H", "S"]:
					all_cards_in_suit = self.cards[suit]
					rank = int(card_info[1])
					for card in all_cards_in_suit:
						if card.rank == rank:
							card_chosen = card
			if card_chosen:
				break
		return card_chosen

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

	def play_you_card(self, message):
		print(message)
		self.print_all_cards()
		card_choice = self.get_you_card_choice()
		self.cards[card_choice.suit].remove(card_choice)
		return card_choice

	def play(self, suit, trump_suit, message):
		if self.isYou:
			return self.play_you_card(message)
		suit_order = self.get_suit_order(suit, trump_suit)
		for s in suit_order:
			if self.cards[s]:
				return self.cards[s].pop()
		return None

	def lead(self, message):
		if self.isYou:
			return self.play_you_card(message)
		suits = ["C", "D", "H", "S"]
		all_cards = self.get_all_cards()
		if len(all_cards) == 0:
			return None
		random.shuffle(all_cards)
		card_choice = all_cards[0]
		self.cards[card_choice.suit].remove(card_choice)
		return card_choice

			







