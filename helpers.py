def convert_card_array(card_array):
	return list(map(lambda card: convert_card_to_str(card), card_array))

def convert_card_to_str(card):
	if card == None:
		return ""
	return card.suit + " " + convert_rank_to_str(card.rank)

def convert_rank_to_str(rank):
	card_rank_str = str(rank)
	special_ranks = {11: "J", 12: "Q", 13: "K", 14: "A"}
	if rank in range(11, 15):
		card_rank_str = special_ranks[rank]
	return card_rank_str

def check_int(string): 
	try: 
		int(string)
		return True
	except ValueError:
		return False

