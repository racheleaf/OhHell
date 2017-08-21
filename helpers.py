def convert_card_array(card_array):
	return list(map(lambda card: convert_card_to_str(card), card_array))

def convert_card_to_str(card):
	if card == None:
		return ""
	return card.suit + " " + str(card.rank)

def check_int(string): 
	try: 
		int(string)
		return True
	except ValueError:
		return False

