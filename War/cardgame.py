import sys
import random

def intro():
	name = input("Hello! What's your name?")

	print("	")

	print("Hi, %s! Welcome to Setback!" %(name))

	print("	")

	print("Do you know how to play?")

	print("	")

	choice_made = False

	while choice_made == False:
		a = input("(Type Y for yes, or N for no) ") 

		if a == "N":
			tutorial = True
			choice_made = True	

		elif a == "Y":
			tutorial = False
			choice_made = True

		else:
			print("	")
			print("Stop trying to break my game! Do you know how to play or not?")
			print("	")

	return tutorial

def tutorial():
	a = 8 # Placeholder

# Create Deck
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

face_cards = ['Jack', 'Queen', 'King', 'Ace']

deck = [[0]*13 for x in range(4)]

for i in range (0, len(suits)):
	for a in range (0, 9):
		deck[i][a] = '%s of %s' %(a+2, suits[i])
	for a in range (9, 13):
		deck[i][a] = '%s of %s' %(face_cards[a-9], suits[i])

def pick_card():
	card = False

	while card == False:
		x = random.randint(0, 3)
		y = random.randint(0, 12)

		a = deck[x][y]

		if a != 0:
			deck[x][y] = 0
			card = True

	return a

hand_a = []
hand_b = []
	
def distribute_hands():

	for c in range (0, 7):
		hand_a.append(pick_card())
		hand_b.append(pick_card())

def print_hand()
	print('Your deck: '+ str(hand_a))


