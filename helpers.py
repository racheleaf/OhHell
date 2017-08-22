def convert_card_array(card_array):
	str_card_array = list(map(lambda card: convert_card_to_str(card), card_array))
	card_array_str = ", ".join(str_card_array)
	return "[" + card_array_str + "]"

def convert_card_to_str(card):
	if card == None:
		return "-"
	return card.suit + " " + convert_rank_to_str(card.rank)

def convert_rank_to_str(rank):
	card_rank_str = str(rank)
	special_ranks = {11: "J", 12: "Q", 13: "K", 14: "A"}
	if rank in range(11, 15):
		card_rank_str = special_ranks[rank]
	return card_rank_str

def convert_bid_array(bid_array, lead, you):
	str_bid_array = list(map(lambda bid: str(bid), bid_array))
	if you > lead:
		for i in range(you, len(bid_array)):
			str_bid_array[i] = "-"
		for i in range(lead):
			str_bid_array[i] = "-"
	else:
		for i in range(you, lead):
			str_bid_array[i] = "-"
	bid_array_str = ", ".join(str_bid_array)
	return "[" + bid_array_str + "]"

def check_int(string): 
	try: 
		int(string)
		return True
	except ValueError:
		return False

