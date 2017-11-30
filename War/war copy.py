'''
Annabelle Strong
9/27/2017

This program runs the card game war for the player to play against the computer

I didn't copy any code from the internet or elsewhere, but I did use the python3 documentation for reference.

Upon my honor, I have neither given nor recieved unauthorized aid. 
'''
###################### IMPORTS ##########################
import sys
import random
import time

######################### GLOBAL VARIABLES ###########################
hand_a = [ ] # User's card array
hand_b = [ ] # Computer's card array

loot_a = [ ] # Extra cards to be won from user in war
loot_b = [ ] # Extra cards to be won from computer in war

acount = 0 # Number of cards in user's hand
bcount = 0 # Number of cards in computer's hand

# Loop logic variables
playing = True
game = True 
number = False

name = "Player 1"

# Number of cards per hand... defaults to 28
n = 28


#################### CARD DISTRIBUTION FUNCTIONS ############################
def create_deck(): # Fills deck array with corresponding cards
	global deck

	suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

	face_cards = ['Jack', 'Queen', 'King', 'Ace']

	deck = [[0]*13 for x in range(4)] # Setting up card deck with 14 card slots for each out of four suits

	# Putting cards in one at a time
	for i in range (0, len(suits)): 
		for a in range (0, 9):
			deck[i][a] = '%s of %s' %(a+2, suits[i])
		for a in range (9, 13):
			deck[i][a] = '%s of %s' %(face_cards[a-9], suits[i])


def pick_card(pile): # Selects random entry from a given array and loops until card is found
	global deck
	global hand_b
	global hand_a
	global game

	card = False

	if pile == hand_a: # Generate random "coordinates" for a card in the user's hand and return the card at that location
		while card == False:

			if len(hand_a) == 1:
				x = random.randint(0, len(hand_a))
			else:
				x = random.randint(0, len(hand_a)-1)

			c = hand_a[x]

			if c != 0: # Replace card with a placeholder 0
				hand_a[x] = 0
				card = True

	elif pile == hand_b: # Generate random "coordinates" for a card in the computer's hand and return the card at that location
		while card == False:

			if len(hand_b) == 1:
				y = random.randint(0, len(hand_b))
			else:
				y = random.randint(0, len(hand_b)-1)

			c = hand_b[y]

			if c != 0: # Replace card with a placeholder 0
				hand_b[y] = 0
				card = True

	else: # Generate random "coordinates" for a card in the deck and return the card at that location
		while card == False:
			j = random.randint(0, 3)
			k = random.randint(0, 12)

			c = deck[j][k]

			if c != 0: # Replace card with a placeholder 0
				deck[j][k] = 0
				card = True

	return c

def add_card(hand, card): # Adds given or random card to given hand
	global hand_a
	global hand_b
	global loot_a
	global loot_b
	global deck

	if card == random:
		card = pick_card(deck)

	if hand == hand_a:
		hand_a.append(card)

	if hand == hand_b:
		hand_b.append(card)

	if hand == loot_a:
		loot_a.append(card)

	if hand == loot_b:
		loot_b.append(card)

def distribute_hands(): # Distributes n number of cards to the two players
	global hand_a
	global hand_b

	# Clear hands in case a game has previously been played
	hand_a = []
	hand_b = []

	# Select m cards from the deck and add them to each hand
	for h in range (0, m):
		add_card(hand_a, random)
		add_card(hand_b, random)

################### CARD CONVERSION FUNCTIONS ##############################
def convert_num(card): # Converts "card notation" to numbers for comparison
	card = str(card)

	# Find the string "of", which can be found in every card entry but not in the slots held by zeroes, and use it 
	# to extract the suit label
	start = card.find('of')-1
	end = len(card)
	suit = card[start:end]

	for i in range (2, 15):
		if i <= 10:					# Set i for number cards down to just their number
			x = card.find(str(i))

		elif i == 11:				# Find face card title and set i to corresponding number
			x = card.find('Jack')

		elif i == 12:
			x = card.find('Queen')

		elif i == 13:
			x = card.find('King')

		elif i == 14:
			x = card.find('Ace')

		if x != -1: 				# If one of the above strings is found (and there is no case where they shouldn't be), replace the card name with i
			card = i
			break

	return [card, suit]

def convert_face(card, suit): # Converts numbers back to "card notation"
	if card <= 10:                  # Recombine the numbers of the number cards and their suit
		card = str(card) + suit

	elif card == 11:				# Translate the face card numbers to titles and recombine with their suit
		card = 'Jack' + suit

	elif card == 12:
		card = 'Queen' + suit

	elif card == 13:
		card = 'King' + suit

	elif card == 14:
		card = 'Ace' + suit

	return card

##################### CARD-VALUE FUCNTIONS #########################
def check_status(): # Checks to see how many, if any, cards are left in the two players' hands
	global game 
	global acount
	global bcount

	# Reset the counting variables so they can be modified to correctly reflect the current hand
	acount = 0 
	bcount = 0

	for x in range (0, len(hand_a)):
		try:							# Attempt to find "of" in all slots of player's hand, which is again unique to cards
			y = hand_a[x].find('of')
			acount += 1					# Increase card count if the string is found

		except AttributeError:			# Maintain card count if error arises from looking for a string in a zero
			acount = acount

	for g in range (0, len(hand_b)):
		try:							# Attempt to find "of" in all slots of the computer's hand, which is again unique to cards
			h = hand_b[g].find('of')
			bcount += 1 				# Increase card count if the string is found

		except AttributeError:			# Maintain card count if error arises from looking for a string in a zero
			bcount = bcount

	if acount or bcount == 0: 			# Check to see if both hands contain cards; end game if one is empty
		game == False


def compare(x, y): # Compares cards played
	global hand_a
	global hand_b
	global loot_a
	global loot_b
	global acount
	global bcount

	# Convert cards to numbers for comparison and save suit for later
	a = int(convert_num(x)[0])
	asuit = convert_num(x)[1]

	b = int(convert_num(y)[0])
	bsuit = convert_num(y)[1]

	compare = True
	war = False

	while compare == True:
		if a < b:
			compare = False

			# Reform full card notation for display
			a = convert_face(a, asuit) 
			b = convert_face(b, bsuit)

			win = b

			# Add both cards to computer's hand if this comparison wasn't a result of a war round
			if war == False:
				add_card(hand_b, a)
				add_card(hand_b, b)

			# Add both cards to computer's hand as well as the bonus cards drawn from the deck during the war round
			else:
				hand_b = hand_b + loot_a + loot_b
				hand_b.append(a)
				hand_b.append(b)

				war = False # End war round

		elif a > b:
			compare = False

			# Reform full card notation for display
			a = convert_face(a, asuit)
			b = convert_face(b, bsuit)

			win = a

			# Add both cards to computer's hand if this comparison wasn't a result of a war round
			if war == False:
				add_card(hand_a, a)
				add_card(hand_a, b)

			# Add both cards to computer's hand as well as the bonus cards drawn from the deck during the war round
			else:
				hand_a = hand_a + loot_a + loot_b
				hand_a.append(a)
				hand_a.append(b)

				war = False # End war round

		elif a == b:
			war = True

			# Account for the cards that have just been compared in the card count variables
			acount -= 1
			bcount -= 1

			print("War! ", end = '')
			time.sleep(.5)

			# Set or pick 2nd showdown card(s) as well as draw bonus cards from the hand if enough cards are availible
			if acount == 0: # Reuse first showdown card since there aren't any left in the hand
				s = a

			elif acount == 1: # Use the only card left as the second showdown code
				s = pick_card(hand_a)

			elif 1 < acount < 4: # Use new card for showdown and any remaining ones as bonus cards
				for i in range (0, acount-1):
					s = pick_card(hand_a)
					add_card(loot_a, pick_card(hand_a))

			elif acount >= 4: # Use new card for showdown and three new ones as bonus cards
				for i in range (0, 3):
					s = pick_card(hand_a)
					add_card(loot_a, pick_card(hand_a))

			# Set or pick 2nd showdown card(s) as well as draw bonus cards from the hand if enough cards are availible
			if bcount == 0: # Reuse first showdown card since there aren't any left in the hand
				p = b

			elif bcount == 1: # Use the only card left as the second showdown code
				p = pick_card(hand_b)

			elif 1 < bcount < 4: # Use new card for showdown and any remaining ones as bonus cards
				for i in range (0, acount-1):
					add_card(loot_b, pick_card(hand_b))
				p = pick_card(hand_b)

			elif bcount >= 4: # Use new card for showdown and three new ones as bonus cards
				for i in range (0, 3):
					add_card(loot_b, pick_card(hand_b))
				p = pick_card(hand_b)

			print('%s vs %s!'%(s, p)) 

			print('	')
			print('Cards to be won:')
			print(loot_a)
			print(loot_b)
			print('	')

			# Convert newly picked showdown cards to numbers for comparison
			n = convert_num(s)
			m = convert_num(p)

			# Save results of conversion in the corresponding variables
			a = int(n[0])
			asuit = n[1]

			b = int(m[0])
			bsuit = m[1]

	return win

################### USER INTERFACE/GAME EXECUTION FUNCTIONS ######################
def tutorial(): # Self-explanitory, though not informative in the least since I spent so much time on everything else...
	time.sleep(.75)
	print("War is a very easy game.")
	time.sleep(.75)
	print("	")
	print("There are two players.")
	time.sleep(.75)
	print("	")
	print("And that's all there is to it! Let's get playing!")
	time.sleep(.75)
	print("	")

def intro(): # Runs once at the beginning of the program to welcome player and launch tutorial if necessary
	global name 

	name = input("Hello! What's your name? ")

	print("	")

	print("Hi, %s! Welcome to War!" %(name))

	print("	")

	print("Do you know how to play?")

	print("	")

	choice_made = False

	while choice_made == False:
		a = input("(Type Y for yes, or N for no) ") 

		if a == 'Y':
			choice_made = True

			print("	")
			print("Excellent! Let's play!")
			print("	")
			break

		elif a == 'N':
			choice_made = True	

			print("	")
			print("Okay! Let me tell you the rules.")
			print("	")
			tutorial()
			break

		else:
			print("	")
			print("Stop trying to break my game! Do you know how to play or not?")
			print("	")

def goodbye(): # Runs when a player's hand no longer contains cards
	if acount == 0:
			print("Oh no! You ran out of cards! You lose.")
	if bcount == 0:
		print("Congratulations! Your opponent ran out of cards! You win!")

	choice = False

	while choice == False:
		print("	")
		x = input("Do you want to play again? (Type Y for yes and N for no) ")

		if x == 'N':
			print("	")
			print("Okay! Thanks for playing!")
			print("	")
			sys.exit()

		elif x == 'Y':
			print("	")
			print("Excellent! Let me shuffle the deck.")
			setup()
			print("	")
			choice = True
			playing = True
			number = False

		else:
			print("	")
			print("Stop trying to break my game! Do you know how to play or not?")


def setup(): # Runs the one-time functions before game starts to prep deck and hands
	acount = 0 
	bcount = 0

	create_deck()
	distribute_hands()
	check_status() # Get number of cards in each deck to send to UI



################################# GAME EXECUTION #####################################

intro()

while playing== True:
	print('*******************************************************************')

	while number == False:
		n = input("How many cards do you want to deal to each hand? (You can choose any number up to 26) ")
		try:
			m = int(n)
			number = True
			game = True
			break

		except (TypeError, ValueError):
			print("	")
			print("Stop trying to break my game! Just answer the question!")
			print("	")
			number = False

	setup()	

	print("	")

	while game == True:
		if acount == 0 or bcount == 0:
				goodbye()
		time.sleep(.4)
		print('*****************************')
		print('YOU HAVE %s CARDS.' %acount)
		print('YOUR OPPONENT HAS %s CARDS.' %bcount)
		print('*****************************')
		print('	')

		card_drawn = False

		g = True

		while card_drawn == False and game == True:
			time.sleep(.7)
			i = input("Hit enter to draw a card from your hand. ")

			if not i:
				card_drawn = True

				a = pick_card(hand_a)
				b = pick_card(hand_b)

				print("	")
				print("Your card: %s" %a)
				print("	")
				time.sleep(1)
				print("Your opponent's card: %s" %b)
				print("	")

				time.sleep(.6)
				print(compare(a, b), end = '')
				print(" wins!")
				print('	')

			else:
				print(" ")
				print("Stop trying to break me! Just draw a card!")
				print("	")

		check_status()
goodbye()


