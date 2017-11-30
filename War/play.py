import sys
import random
import time
from war import create_deck, distribute_hands, pick_card, add_card, convert_num, convert_face, compare, check_status

# GLOBALS
playing = True
game = True

name = "Player 1"

hand_a = [ ]
hand_b = [ ]

from war import acount
from war import bcount

loot_a = [ ]
loot_b = [ ]

deck = [[0]*13 for x in range(4)]



#########################################################################################

intro()

print('*******************************************************************')

while playing== True:

	setup()	

	while game == True:
		check_status()
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

		#game = bool(check_status() == 'none')

goodbye(check_status())

