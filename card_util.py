import random
import helpers
import math

class Card: 

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

class Deck:

	def __init__(self):
		suits = ("C", "D", "H", "S")
		ranks = range(2, 15)
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

	def __init__(self, isYou, num_players):
		self.cards = {
			"C": [],
			"D": [],
			"H": [],
			"S": [],
		}
		self.isYou = isYou
		self.num_players = num_players

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
		self.cards[card.suit].sort(key = lambda card: card.rank)

	# def get_suit_order(self, suit, trump_suit): 
	# 	suits = ["C", "D", "H", "S"]
	# 	suit_order = [suit]
	# 	suits.remove(suit)
	# 	if (suit != trump_suit):
	# 		suit_order.append(trump_suit)
	# 		suits.remove(trump_suit)
	# 	random.shuffle(suits)
	# 	suit_order += suits
	# 	return suit_order

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
					rank = card_info[1].upper()
					for card in all_cards_in_suit:
						if helpers.convert_rank_to_str(card.rank) == rank:
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

	def play(self, lead_suit, trump_suit, cards_played_so_far, lead, num_tricks_needed):
		if self.isYou:
			card_str_array = helpers.convert_card_array(cards_played_so_far)
			message_beginning = "Player " + str(lead + 1) + " led with " + card_str_array[lead] + ". "
			message_beginning += "So far the cards played are:"
			print(message_beginning, card_str_array)
			return self.play_you_card(lead_suit)
		valid_cards = self.cards[lead_suit]
		if not valid_cards:
			valid_cards = self.get_all_cards()
		best_card = None
		closest_est_tricks_take = math.inf
		for card in valid_cards:
			est_tricks_take = 0
			est_tricks_take += self.get_prob_card_takes(card, lead_suit, trump_suit)
			est_tricks_take += self.approx_win_tricks(trump_suit, card)
			if math.fabs(est_tricks_take - num_tricks_needed) < closest_est_tricks_take:
				best_card = card
				closest_est_tricks_take = est_tricks_take
		return best_card

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

	def get_bid(self, trump_suit, bids, restriction):
		if self.isYou:
			self.print_all_cards()
			num_cards = len(self.get_all_cards())
			bid = 0
			print("Here are the bids so far: (-1 means hasn't bet)", bids)
			bid_str = input("Please bid the number of tricks you think you will take: ")
			while True:
				if helpers.check_int(bid_str) and int(bid_str) >= 0 and int(bid_str) <= num_cards:
					if int(bid_str) != restriction:
						bid = int(bid_str)
						break
					bid_str = input("Sorry, you cannot bid that number. Please bid a different number: ")
				else:
					bid_str = input("Please input a valid bid: ")
			return bid
		bid = math.floor(self.approx_win_tricks(trump_suit))
		if bid == restriction:
			if bid > 0:
				bid -= 1
			else:
				bid += 1
		return bid

	def approx_win_tricks(self, trump_suit, removed_card = None):
		exp_tricks = 0
		all_cards = self.get_all_cards()
		if removed_card and removed_card in all_cards:
			all_cards.remove(removed_card)
		num_cards = len(all_cards)
		for card in all_cards:
			exp_tricks += self.get_prob_card_max_in_suit(card) * min(num_cards / 4, 1)
		suits = ["C", "D", "H", "S"]
		# tricks_trumped = 0
		# for suit in suits:
		# 	if suit != trump_suit:
		# 		suit_length = len(self.cards[suit])
		# 		exp_cards_in_suit = num_cards / num_players
		# 		tricks_trumped += max(exp_cards_in_suit - suit_length, 0)
		# tricks_trumped = min(tricks_trumped, len(self.cards[trump_suit]))
		# exp_tricks += tricks_trumped
		return exp_tricks

	def get_prob_card_takes(self, card, lead_suit, trump_suit):
		prob_card_max_in_suit = self.get_prob_card_max_in_suit(card)
		num_cards = len(self.get_all_cards())
		if lead_suit == trump_suit:
			if card.suit == lead_suit:
				return prob_card_max_in_suit
			return 0
		if card.suit == lead_suit:
			return prob_card_max_in_suit * min(num_cards / 4, 1)
		if card.suit == trump_suit:
			return min(prob_card_max_in_suit / self.num_players * 4, 1)
		return 0


	def get_prob_card_max_in_suit(self, card):
		all_cards = self.get_all_cards()
		num_cards = len(all_cards)
		prob_card_exists = self.num_players * num_cards / 52
		return (1 - prob_card_exists) ** (14 - card.rank)

			







