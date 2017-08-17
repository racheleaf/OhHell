import card_util
from functools import reduce

class Game:

	def __init__(self, num_players):
		self.num_players = num_players
		self.round = 1
		self.trump_suit = "C"
		self.dealer = 0
		self.you = 0
		self.hands = []
		for i in range(num_players):
			self.hands.append(card_util.Hand())

	def reset_deck(self):
		suits = ("C", "D", "H", "S")
		ranks = range(1, 14)
		self.deck = card_util.Deck(suits, ranks)
		self.deck.shuffle()

	def deal(self, num_cards):
		self.deck.deal(self.hands, num_cards, self.dealer)

	def play_round(self):
		num_cards = self.round
		self.reset_deck()
		for hand in self.hands:
			hand.reset()
		self.deal(num_cards)
		self.trump_suit = self.deck.get_card().suit
		lead = (self.dealer + 1) % self.num_players
		for trick in range(num_cards):
			lead_suit, complete_trick = self.play_trick(lead)
			print("trick", lead_suit, self.trump_suit)
			for card in complete_trick:
				print(card.suit, card.rank)
		self.round += 1

	def play_trick(self, lead): 
		cards_played = [None] * self.num_players
		cards_played[lead] = self.hands[lead].lead()
		lead_suit = cards_played[lead].suit
		for i in range(lead + 1, lead + self.num_players):
			player = i % self.num_players
			cards_played[player] = self.hands[player].play(lead_suit, self.trump_suit)
		return lead_suit, cards_played

	#returns negative number if card1 < card2, positive number if card1 > card2
	def compare_cards(card1, card2, lead_suit):
		top_suits = [lead_suit, this.trump_suit]
		suit_strength1 = top_suits.index(card1.suit)
		suit_strength2 = top_suits.index(card2.suit)
		return suit_strength1 - suit_strength2 || card1.rank - card2.rank

	def get_winner(self, cards_played, lead_suit):
		winner = 0
		

