from os import system,name
from random import choice

#self defined console clear
def clear():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')

#general horizontal win check
def checkHorizontal(board,i):
	j = 1
	if board[i] == board[i+j] and board[i] == board[i+j*2]:
		return True
	else:
		return False

#general vertical win check
def checkVertical(board,i):
	j = 3
	if board[i] == board[i+j] and board[i] == board[i+j*2]:
		return True
	else:
		return False

class Game:
	def __init__(self,num):
		#the boarddata
		if num:
			self.board = [str(i) for i in range(9)]
		else:
			self.board = [' ' for i in range(9)]
		#the leftover fields
		self.fields = [i for i in range(9)]
		#to determine who starts and which player is active
		self.comTurn = choice([True,False])

	def drawBoard(self,board):
		print('#'*13)
		print('# '+board[0]+' # '+board[1]+' # '+board[2]+' #')
		print('#'*13)
		print('# '+board[3]+' # '+board[4]+' # '+board[5]+' #')
		print('#'*13)
		print('# '+board[6]+' # '+board[7]+' # '+board[8]+' #')
		print('#'*13)

	def initializePlayers(self):
		inputName = input('Insert your name: ')
		self.human = Player(inputName,'O')
		self.com = Player('Computer','X')

	def inputTurn(self,player):
		if not Tic.comTurn:
			field = int(input('Choose a field: '))
			while field not in self.fields:
				field = int(input('This field does not exist or is already set. Choose another: '))
		else:
			field = choice(self.fields)
		self.fields.remove(field)
		self.board[field] = player.char
		self.comTurn = not self.comTurn

	def checkWin(self):
		win = 0
		for i in range(len(self.board)):

			#checks for field 1
			if i == 0:
				if checkHorizontal(self.board,i):
					win = self.determineWinner(i)
				elif checkVertical(self.board,i):
					win = self.determineWinner(i)
				#check diagonal
				elif self.board[i] == self.board[i+4] and self.board[i] == self.board[i+8]:
					win = self.determineWinner(i)

			#checks for field 2
			elif i == 1:
				if checkVertical(self.board,i):
					win = self.determineWinner(i)

			#checks for field 3
			elif i == 2:
				if checkVertical(self.board,i):
					win = self.determineWinner(i)
				#check diagonal
				elif self.board[i] == self.board[i+2] and self.board[i] == self.board[i+4]:
					win = self.determineWinner(i)

			#checks for field 4
			elif i == 3:
				if checkHorizontal(self.board,i):
					win = self.determineWinner(i)

			#checks for field 7
			elif i == 6:
				if checkHorizontal(self.board,i):
					win = self.determineWinner(i)

		return win

	def determineWinner(self,i):
		if self.board[i] == self.human.char:
			return self.human
		elif self.board[i] == self.com.char:
			return self.com
		else:
			return 0

class Player:
	def __init__(self,inputName,inputChar):
		self.name = inputName
		self.char = inputChar


clear()
#ask for field numbering
while True:
	num = input('Do you want to enable field numbering? (Type "yes" or "no") ')
	if num == 'yes' or num == 'Yes':
		Tic = Game(True)
		break
	elif num == 'no' or num == 'No':
		Tic = Game(False)
		break
#initalize the two players and ask for a playername
Tic.initializePlayers()
#the game loop
while True:
	clear()
	Tic.drawBoard(Tic.board)
	if not Tic.comTurn:
		Tic.inputTurn(Tic.human)
	else:
		Tic.inputTurn(Tic.com)
	winner = Tic.checkWin()
	#determine the winner
	if winner == Tic.human:
		clear()
		Tic.drawBoard(Tic.board)
		print(Tic.human.name+' has won the game!')
		break
	elif winner == Tic.com:
		clear()
		Tic.drawBoard(Tic.board)
		print(Tic.com.name+' has won the game!')
		break
	#check for draw
	if len(Tic.fields) == 0:
		clear()
		Tic.drawBoard(Tic.board)
		print('The game is a draw!')
		break