import card_util
from functools import reduce

class Game:

	def __init__(self, num_players):
		self.num_players = num_players
		self.round = 1
		self.dealer = 0
		self.you = 0
		self.score = [0] * num_players
		self.hands = []
		self.turnaround_num_cards = 51 // num_players
		for i in range(num_players):
			self.hands.append(card_util.Hand(i == self.you))

	def prepare_deck(self): 
		suits = ("C", "D", "H", "S")
		ranks = range(1, 14)
		deck = card_util.Deck(suits, ranks)
		deck.shuffle()
		return deck

	def play(self):
		play_next_round = True
		while play_next_round:
			play_next_round = False
			done = False
			while not done:
				message = "Are you ready for the next trick? (Y/N) "
				if self.round == 1:
					message = "Are you ready to play the first trick? (Y/N) "
				reply = input(message)
				if reply == "Y" or reply == "N":
					done = True
					play_next_round = (reply == "Y")
			if not play_next_round:
				print("The final score is", self.score)
			else:
				num_tricks = max(self.round, self.round - self.turnaround_num_cards)
				self.play_round(self.round)

	def play_round(self, num_tricks):
		tricks_taken = [0] * self.num_players
		deck = self.prepare_deck()
		for hand in self.hands:
			hand.reset()
		deck.deal(self.hands, num_tricks, self.dealer)
		trump_suit = deck.get_card().suit
		lead = (self.dealer + 1) % self.num_players
		for trick in range(num_tricks):
			lead_suit, cards_played = self.get_trick_info(lead, trump_suit)
			print("trick", lead_suit, trump_suit)
			for card in cards_played:
				print(card.suit, card.rank)
			winner = self.get_winner(cards_played, lead_suit, trump_suit)
			tricks_taken[winner] += 1
			lead = winner
		print(tricks_taken)
		for i in range(self.num_players):
			self.score[i] += tricks_taken[i]
		self.round += 1

	def get_trick_info(self, lead, trump_suit): 
		cards_played = [None] * self.num_players
		lead_message = "You lead this trick. Pick a card to play： "
		cards_played[lead] = self.hands[lead].lead(lead_message)
		lead_suit = cards_played[lead].suit
		for i in range(lead + 1, lead + self.num_players):
			player = i % self.num_players
			message = "The current suit is " + lead_suit + " and the trump suit is " + trump_suit +"."
			cards_played[player] = self.hands[player].play(lead_suit, trump_suit, message)
		return lead_suit, cards_played

	# returns negative number if card1 < card2, positive number if card1 > card2
	def compare_cards(self, card1, card2, lead_suit, trump_suit):
		if card1.suit == card2.suit:
			return card1.rank - card2.rank
		if card1.suit == trump_suit:
			return 1
		if card2.suit == trump_suit:
			return -1
		if card1.suit == lead_suit:
			return 1
		if card2.suit == lead_suit: 
			return -1
		return 0

	def get_winner(self, cards_played, lead_suit, trump_suit):
		winner = 0
		for i in range(len(cards_played)):
			card = cards_played[i]
			max_card = cards_played[winner]
			if self.compare_cards(card, max_card, lead_suit, trump_suit) > 0:
				winner = i
		return winner
		

