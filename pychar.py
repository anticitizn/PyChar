from bresenham import bresenham

class Terminal:
	def __init__(self, name, columns, rows, char):
		self.columns = columns
		self.rows = rows
		self.container = []
		self.name = name
		i = 0
		while i < int(rows*columns):
			self.container.append(char)
			i += 1

		#the terminal is stored in a single list

	def flush(self):
		print()
		i = 1
		o = 0
		self.tempcont = ""
		while i <= self.rows:
			tempcont = ""
			while o < self.columns*i:
				tempcont = tempcont + self.container[o] + " "
				o += 1
			i += 1
			print(tempcont)

		#prints out the contents of the terminal in a readable way


	#def flush(self):
	#	i = 0
	#	self.tempcont = ""
	#	while i <= self.rows:
	#		count1 = i*self.columns
	#		count2 = count1 + self.columns
	#		self.tempcont += ' '.join(self.container)[count1:count2]
	#		self.tempcont += "\n"
	#		i += 1
	#	print(self.tempcont)

	def inverseCoord(self, x1, x2, y1, y2):
		self.x1new = x1
		self.x2new = x2
		self.y1new = y1
		self.y2new = y2
		if x1-x2 < 0:
			self.x1new = x2
			self.x2new = x1
		if y1-y2 < 0:
			self.y1new = y2
			self.y2new = y1
		return(self.x1new, self.x2new, self.y1new, self.y2new)

		#checks for any coordinates where x2 is smaller than x1
		#or y2 than y1 and reverses them for convenience

	def getChar(self, x, y):
		return(self.container[self.returnOrder(x, y)])

	def blit(self, otherTerminal, xnew, ynew, x1old, x2old, y1old, y2old):
		self.xnew = xnew
		self.ynew = ynew
		self.x1old, self.x2old, self.y1old, self.y2old = self.inverseCoord(x1old, x2old, y1old, y2old)
		i = y2old - y1old
		while i >= 0:
			o = x2old - x1old
			while o >= 0:
				self.putChar(xnew + o, ynew + i, otherTerminal.getChar(x1old+o, y1old+i))
				o -= 1
			i -= 1

		#pastes one terminal's content inside another

	def putChar(self, x, y, char):
		self.container[self.returnOrder(x, y)] = char

		#changes a single char on the terminal

	def returnOrder(self, x, y):
		return x+y*self.columns

		#returns the exact index of the char with these coordinates

	def drawLine(self, x1, y1, x2, y2, char):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.char = char
		coords = list(bresenham(x1, y1, x2, y2))
		for coord in coords:
			self.putChar(coord[0], coord[1], char)

		#draws a line, uses the bresenham library because
		#im too lazy to do it myself right now

	def drawRect(self, x1, x2, y1, y2, char, filled=False):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.char = char
		self.filled = filled
		self.drawLine(x1, y1, x2, y1, char)
		self.drawLine(x1, y2, x2, y2, char)
		self.drawLine(x1, y1, x1, y2, char)
		self.drawLine(x2, y1, x2, y2, char)
		if filled == True:
			i = y2 - y1
			o = 0
			while o < i:
				self.drawLine(x1, y2-o, x2, y2-o, char)
				o += 1


"""
	#these shouldnt be in the terminal renderer itself but might be useful

    def save(self):
        file = open("testsave.txt","w")
        file.write(''.join(self.container))

    def load(self, loadname):
        file = open(loadname,"r")
        self.container = list(file.read(self.columns*self.rows))
"""
def testScript():
	term1 = Terminal("term1", 14, 12, "x")
	term2 = Terminal("term2", 14, 12, "f")
	term1.drawLine(2, 0, 1, 3, "O")
	term1.drawRect(5, 2, 10, 8, "S", filled=True)
	term1.flush()
	print()
	term1.blit(term2, 0, 0, 0, 13, 0, 11)
	term1.flush()
	print(''.join(term1.container))
	print()
	input()

if __name__ == '__main__':
	testScript()