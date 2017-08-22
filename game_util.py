import card_util
from functools import reduce
import helpers

class Game:

	def __init__(self, num_players):
		self.num_players = num_players
		self.round_number = 1
		self.dealer = 0
		self.you = 0
		self.scores = [0] * num_players
		self.hands = []
		self.turnaround_num_cards = 51 // num_players
		for i in range(num_players):
			self.hands.append(card_util.Hand(i == self.you))

	def prepare_deck(self): 
		deck = card_util.Deck()
		deck.shuffle()
		return deck

	def play(self):
		print("Your game has been created. You are player " + str(self.you + 1) + ".")

		play_next_round = True
		while play_next_round:
			play_next_round = False
			done = False
			while not done:
				message = "Do you want to play another round? (Y/N) "
				if self.round_number == 1:
					message = "Are you ready to play the first round? (Y/N) "
				reply = input(message).strip().upper()
				if reply == "Y" or reply == "N":
					done = True
					play_next_round = (reply == "Y")
			if not play_next_round:
				print("Thank you for playing! The final scores are", self.scores)
				winners_list = self.get_overall_winners()
				if len(winners_list) == 1:
					print("The winner is player " + str(winners_list[0] + 1) + ".")
				else:
					print("Players", ", ".join(list(map(lambda winner: str(winner + 1), winners_list))), " tied for first.")
				if self.you in winners_list:
					print("Congratulations!")
			else:
				num_tricks = max(self.round_number, self.round_number - self.turnaround_num_cards)
				self.play_round(self.round_number)

	def play_round(self, num_tricks):
		tricks_taken = [0] * self.num_players
		deck = self.prepare_deck()
		for hand in self.hands:
			hand.reset()
		deck.deal(self.hands, num_tricks, self.dealer)
		trump_suit = deck.get_card().suit
		lead = (self.dealer + 1) % self.num_players

		round_str_ending = "th"
		round_str = str(self.round_number)
		if round_str[-1] == "1":
			round_str_ending = "st"
		elif round_str[-1] == "2":
			round_str_ending = "nd"
		num_tricks_ending = "s"
		if num_tricks == 1:
			num_tricks_ending = ""
		welcome_message = "ROUND " + round_str + ":\n"
		welcome_message += "Welcome to the " + round_str + round_str_ending + " round of Oh Hell. "
		welcome_message += "This round consists of " + str(num_tricks) + " trick" + num_tricks_ending + ". "
		welcome_message += "The trump suit is " + trump_suit + "."
		print(welcome_message)

		print("BIDDING: ")
		bids = self.get_bids(trump_suit, num_tricks)
		print("Here are everyone's bids:", bids)
		
		for trick in range(num_tricks):
			lead_suit, cards_played = self.get_trick_info(lead, trump_suit, trick)
			winner = self.get_trick_winner(cards_played, lead_suit, trump_suit)
			tricks_taken[winner] += 1
			lead = winner
			print("Cards played:", helpers.convert_card_array(cards_played))
			print("Winner: Player", (winner + 1))
		print("The round is over. Here are the number of tricks each player took:", tricks_taken)
		score_update = self.get_score_update(bids, tricks_taken)
		print("Each player will get awarded this many points for the round:", score_update)
		self.update_scores(score_update)
		print("The current scores are:", self.scores)

		self.round_number += 1
		self.dealer += 1
		self.dealer %= self.num_players

	def get_bids(self, trump_suit, num_tricks):
		lead = (self.dealer + 1) % self.num_players
		bids = [0] * self.num_players
		for i in range(lead, lead + self.num_players):
			player = i % self.num_players
			restriction = -1
			if i % self.num_players == self.dealer:
				sum_bids = reduce(lambda total, bid: total + bid, bids)
				restriction = num_tricks - restriction
			bids[player] = self.hands[player].get_bid(trump_suit, self.num_players, restriction)
		return bids

	def get_trick_info(self, lead, trump_suit, trick_number): 
		print("TRICK " + str(trick_number + 1) + ":")
		cards_played = [None] * self.num_players
		cards_played[lead] = self.hands[lead].lead()
		lead_suit = cards_played[lead].suit
		for i in range(lead + 1, lead + self.num_players):
			player = i % self.num_players
			cards_played[player] = self.hands[player].play(lead_suit, trump_suit, cards_played, lead)
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

	def get_trick_winner(self, cards_played, lead_suit, trump_suit):
		winner = 0
		for i in range(len(cards_played)):
			card = cards_played[i]
			max_card = cards_played[winner]
			if self.compare_cards(card, max_card, lead_suit, trump_suit) > 0:
				winner = i
		return winner
		
	def get_overall_winners(self): 
		winners = [0]
		for i in range(1, self.num_players):
			top_score = self.scores[winners[0]]
			if self.scores[i] > top_score:
				winners = [i]
			elif self.scores[i] == top_score:
				winners.append(i)
		return winners

	def get_score_update(self, bids, tricks_taken):
		score_update = [0] * self.num_players
		for i in range(self.num_players):
			if bids[i] == tricks_taken[i]:
				score_update[i] += 10
			score_update[i] += tricks_taken[i]
		return score_update

	def update_scores(self, score_update):
		for i in range(self.num_players):
			self.scores[i] += score_update[i]

