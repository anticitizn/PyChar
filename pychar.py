from bresenham import bresenham

class Terminal:
	def __init__(self, columns, rows, char):
		self.columns = columns
		self.rows = rows
		self.container = []
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

		#prints out the contents of the terminal

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

	def drawRect(self, x1, y1, x2, y2, char):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.char = char
		self.drawLine(x1, y1, x2, y1, char)
		self.drawLine(x1, y2, x2, y2, char)
		self.drawLine(x1, y1, x1, y2, char)
		self.drawLine(x2, y1, x2, y2, char)

		#summons satan

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
	term1 = Terminal(14, 12, "x")
	term1.drawLine(2, 0, 1, 3, "O")
	term1.drawRect(5, 2, 10, 8, "S")
	term1.flush()
	print()
	print(''.join(term1.container))
	print()
	input()

testScript()
