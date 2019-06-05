import curses
import random
import time

words = ['turtle', 'good', 'match', 'moist', 'height']

screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.curs_set(0)

dims = screen.getmaxyx()

score = 0
mi = 32
ma = 122
index = 0

desired = list(random.choice(words))
current = [' ' for i in range(len(desired))]

xi = int(dims[1]/2 - len(desired))
xf = int(dims[1]/2 - 1)
y = int(dims[0]/2)

class Letter(object):

    """Falling letter"""

    def __init__(self, w):
        self.word = w
        self.restart()

    def restart(self):
        self.char = random.choice(self.word)
        self.x = random.randint(1, dims[1]-2)
        self.y = random.randint(-50, 0)
        self.cd = 0

    def update(self):
        if(self.cd >= 100):
            self.cd = 0
            self.y += 1
            if(self.y == dims[0]):
                # current[self.x - xi] = self.char
                self.restart()
        else:
            self.cd += 1

    def display(self):
        if(self.y >= 1):
            screen.addstr(self.y-1, self.x, ' ')
            screen.addstr(self.y, self.x, self.char)

class Word(object):

    """Word"""

    def __init__(self):
        self.score = 0
        self.obj = random.choice(words)
        self.cur = [' ' for i in range(len(self.obj))]
        self.x = int(dims[1]/2 - len(self.obj))
        self.y = int(dims[0]/2)

    def move(self, x, y):
        screen.addstr(self.y, self.x, ' ' * len(self.obj))
        self.x += x
        self.y += y

    def inWord(self, letter):
        if(self.y == letter.y and self.x <= letter.x < self.x + len(self.obj)):
            self.cur[letter.x - self.x] = letter.char

    def display(self):
        screen.addstr(self.y, self.x, ''.join(self.cur), curses.A_REVERSE)

    def update(self, char, idx):
        self.cur[idx] = char

    def getScore(self):
        self.score = 0
        for i in range(len(self.obj)):
            if(self.cur[i] == self.obj[i]):
                self.score += 1 
        return str(self.score)

    def getWord(self):
        return ''.join(self.obj)


        

word = Word()
letters = [Letter(word.getWord()) for i in range(20)]

cd = 0

while True:
    q = screen.getch()
    screen.border(0)
    screen.addstr(0, 2, 'Score: ' + word.getScore())
    screen.addstr(0, dims[1] - len(word.obj) - 8, 'Word: ' + word.getWord())

    for l in letters:
        if(score < len(desired)):
            l.display()
            l.update()
            word.inWord(l)

    word.display()

    if(q > 0):
        if(chr(q) == 'h' or q == curses.KEY_LEFT):
            word.move(-1, 0)
        if(chr(q) == 'j' or q == curses.KEY_DOWN):
            word.move(0, 1)
        if(chr(q) == 'k' or q == curses.KEY_UP):
            word.move(0, -1)
        if(chr(q) == 'l' or q == curses.KEY_RIGHT):
            word.move(1, 0)
        if(chr(q) == 'q'):
            break

    screen.refresh()
    time.sleep(0.001)
curses.endwin()

