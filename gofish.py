#!/usr/bin/python3
import pickle
import random

spadesCardList=[]
heartsCardList=[]
diamondsCardList=[]
clubsCardList=[]

for number in range(13):
	spadesCardList.append(number+1)
for number in range(13):
	heartsCardList.append(number+1)
for number in range(13):
	diamondsCardList.append(number+1)
for number in range(13):
	clubsCardList.append(number+1)

deck={1:spadesCardList,2:heartsCardList,
3:diamondsCardList,4:clubsCardList}

playerNumber=input('How many people are playing?')
playerNumber=int(playerNumber)
players = []
playerPoints=[]
for i in range(playerNumber):
	playerPoints.append(0)
for i in range(playerNumber):
	players.append({})
for player in range(playerNumber):
	for suit in range(4):
		players[player][suit+1]=[]

if playerNumber==2:
	for player in players:
		for i in range(7):
			suit=random.randint(1,4)
			while len(deck[suit]) == 0:
				suit=random.randint(1,4)
			cardNumber=random.choice(deck[suit])
			player[suit].append(cardNumber)
			deck[suit].remove(cardNumber)
if playerNumber>2:
	for player in players:
		for i in range(5):
			suit=random.randint(1,4)
			while len(deck[suit]) == 0:
				suit=random.randint(1,4)
			cardNumber=random.choice(deck[suit])
			player[suit].append(cardNumber)
			deck[suit].remove(cardNumber)

print(deck)
for player in players:
	print(player)
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

running = True
playerTurn = 0

def checkWhoWon():
	highestPoints = 0
	for point in playerPoints:
		if point > highestPoints:
			highestPoints=point
	counter=0
	winners=[]
	for point in playerPoints:
		if point == highestPoints:
			winners.append(counter+1)
			counter+=1
	if len(winners)==1:
		print('Player', winner[0],'won!')
	else:
		for winner in winners:
			winnerText= winnerText+'and'+str(i)
		print('Players',winnerText,'won!')
while running:
	print('It is player ',playerTurn+1,"'s turn")
	print(players[playerTurn])

	#Finds which player and card to try and retrieve
	if len(players)>2:
		playerAsk = input('What player do you want to ask?')
		while (int(playerAsk)-1)%playerNumber==playerTurn or int(playerAsk)>len(players):
			playerAsk = input('The player number you provided is invalid.')
	else:
		playerAsk = (playerTurn + 1) % playerNumber
		print('automatically asking player',playerAsk+1)
		playerAsk=int(playerAsk)+1
	playerAsk=int(playerAsk)
	cardNumber= input('What card number do you want?')
	while len(str(cardNumber))==0:
		cardNumber=input("The length of your response can not equal 0.")
	cardNumber=int(cardNumber)
	while int(cardNumber>13):
		cardNumber=input('The card number can not be greater than 13.')
	cardNumber=int(cardNumber)

	#Adds card if other player has it
	newCard=False
	Break=False
	for i in range(4):
		if Break==False:
			for card in players[playerAsk-1][i+1]:
				if card==cardNumber and Break==False:
					players[playerTurn][i+1].append(card)
					players[playerAsk-1][i+1].remove(card)
					newCard=True
					if i+1==1:
						suit='spades'
					if i+1==2:
						suit='hearts'
					if i+1==3:
						suit='diamonds'
					if i+1==4:
						suit='clubs'								
					print('You have recieved the',cardNumber,'of',suit)
					Break=True

	#go fish if other player doesn't have card
	if newCard == False:
		print('You have to go fish')
		suit=random.randint(1,4)
		while len(deck[suit]) == 0:
			suit=random.randint(1,4)
		cardNumber=random.choice(deck[suit])
		players[playerTurn][suit].append(cardNumber)
		deck[suit].remove(cardNumber)
		print(players)
		print(deck)

	#Checks for a set of 4 cards
	cardSet = 0
	for key,items in players[playerTurn].items():
		for card in items:
			cardCounter+=1
			if card==cardNumber:
				cardSet+=1
	if cardSet==4:
		playerPoints[playerTurn]+=1
		for key,items in players[playerTurn].items():
			for card in items:
				if card==cardNumber:
					players[playerTurn][suit+1].remove(card)
		print('Player',playerTurn+1,'had a set of',cardNumber,'s. They earned a point')
	cardSet=0

	#checks for an empty deck
	emptyDeck = 0
	for suit in deck:
		if len(deck[suit])==0:
			emptyDeck+=1
	if emptyDeck == 4:
		checkWhoWon()
		running=False
	else:
		emptyDeck = 0

	#checks for an empty hand
	emptyHand=0
	for hand in players:
		for suit in hand:
			if len(hand.get(suit))==0:
				emptyHand+=1
		if emptyHand==4:
			checkWhoWon()
			running=False
		else:
			emptyHand=0

	playerTurn = (playerTurn + 1) % playerNumber
