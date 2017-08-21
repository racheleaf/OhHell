import random
import helpers

class Card: 

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

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
		card_str_array = helpers.convert_card_array(all_cards)
		print("Your cards:", card_str_array)

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

	def check_valid_play(self, card, lead_suit):
		if not lead_suit:
			return True
		if card.suit == lead_suit:
			return True
		if not len(self.cards[lead_suit]):
			return True
		return False

	def get_you_card_choice(self, lead_suit):
		card_chosen = None
		card_str = input("Pick a card to play: ").strip()
		while True:
			card_info = card_str.split(" ")
			if len(card_info) == 2:
				suit = card_info[0].upper()
				if suit in ["C", "D", "H", "S"]:
					all_cards_in_suit = self.cards[suit]
					rank = card_info[1]
					for card in all_cards_in_suit:
						if str(card.rank) == rank:
							card_chosen = card
			elif len(card_info) == 1:
				if helpers.check_int(card_str):
					card_index = int(card_str)
					all_cards = self.get_all_cards()
					if card_index > 0 and card_index <= len(all_cards):
						card_chosen = all_cards[card_index - 1]
			if card_chosen:
				card_valid = self.check_valid_play(card_chosen, lead_suit)
				if card_valid:
					break
				card_chosen = None
			card_str = input("The card choice is not valid. Please try again: ").strip()
		return card_chosen

	def play_you_card(self, lead_suit):
		self.print_all_cards()
		card_choice = self.get_you_card_choice(lead_suit)
		self.cards[card_choice.suit].remove(card_choice)
		return card_choice

	def play(self, suit, trump_suit, cards_played_so_far, lead):
		if self.isYou:
			card_str_array = helpers.convert_card_array(cards_played_so_far)
			message_beginning = "Player " + str(lead + 1) + " led with " + card_str_array[lead] + ". "
			message_beginning += "So far the cards played are:"
			print(message_beginning, card_str_array)
			return self.play_you_card(suit)
		suit_order = self.get_suit_order(suit, trump_suit)
		for s in suit_order:
			if self.cards[s]:
				return self.cards[s].pop()
		return None

	def lead(self):
		if self.isYou:
			print("You lead this trick. Pick a card to play.")
			return self.play_you_card(None)
		suits = ["C", "D", "H", "S"]
		all_cards = self.get_all_cards()
		if len(all_cards) == 0:
			return None
		random.shuffle(all_cards)
		card_choice = all_cards[0]
		self.cards[card_choice.suit].remove(card_choice)
		return card_choice

			







