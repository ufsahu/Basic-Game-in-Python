#Importing all the required modules
import sys
import random
from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Canvas, ALL, NW

#Setting up the game variables
WIDTH = 300
HEIGHT = 300
DELAY = 70
DOT_SIZE = 10
ALL_DOTS = WIDTH * HEIGHT / (DOT_SIZE * DOT_SIZE)
RAND_POS = 27

#All possible X and Y coordinates of snake dots (connectors)
x = [0] * ALL_DOTS
y = [0] * ALL_DOTS


class Board(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT,
                        background="white", highlightthickness=0)

        self.parent = parent
        self.initGame()
        self.pack()

    #Initializes variables, loads images and runs the timer function.
    def initGame(self):

        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.inGame = True
        self.dots = 3

        self.apple_x = 100
        self.apple_y = 190

        for i in range(self.dots):
            x[i] = 50 - i * 10
            y[i] = 50

        # Loading our images. These are three images for our game:
        # head, dot(body or connection) and apple.
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.iapple)
        # Error handling
        except IOError, e:
            print e
            sys.exit(1)

        self.focus_get()
        # The createObject () method creates objects on the canvas,
        # and locateApple () sets the apple to a random point on the canvas.
        self.createObjects()
        self.locateApple()
        # Assigning keyboard keys using the onKeyPressed () method.
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(DELAY, self.onTimer)

    # Creating the game objects on the canvas. These are canvas objects.
    # They have starting X and Y coordinates. The "image" option allows
    # images to appear on the canvas. The "anchor" parameter is set to
    # NW (North West), which means a reference to the upper left point of the canvas.
    # The "tag" parameter is used to identify objects on the canvas.
    # One tag can be used for several objects on the canvas.The checkApple()
    # method allows us to find out if the snake ate an apple object.
    # If so, we add one snake connection and run locateApple().
    def createObjects(self):

        self.create_image(self.apple_x, self.apple_y, image=self.apple, anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")

    def checkApple(self):

        # Allows us to find an object on the canvas using this tag.
        # We need two objects: the head of a snake and an apple.
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        # Returns the points of the boundaries of the object.
        # Using the find_overlapping () method, we know the
        # collision of objects with these coordinates.
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        # If an apple encounters a head, we create a new connection
        # for the snake on the coordinates of the apple.
        # Also, we run the locateApple() method, which removes
        # the old apple from the canvas and creates a new one at a random point.
        for ovr in overlap:

            if apple[0] == ovr:
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locateApple()

    # Turn on the game key algorithms.
    # All body connections of the snake move behind the head as one single chain.
    def doMove(self):

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        items = dots + head

        # Allows the connections to move in the same chain.
        z = 0
        while z < len(items) - 1:
            c1 = self.coords(items[z])
            c2 = self.coords(items[z + 1])
            self.move(items[z], c2[0] - c1[0], c2[1] - c1[1])
            z += 1

        # The movement of the snake's head to the left.
        if self.left:
            self.move(head, -DOT_SIZE, 0)
        # The movement of the snake's head to the right.
        if self.right:
            self.move(head, DOT_SIZE, 0)
        # The movement of the snake's head up.
        if self.up:
            self.move(head, 0, -DOT_SIZE)
        # The movement of the snake's head down.
        if self.down:
            self.move(head, 0, DOT_SIZE)

    # Determine when the snake strikes itself or one of the walls.
    def checkCollisions(self):

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        # Snake hits own body.
        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False
        # Snake hits the walls.
        if x1 < 0:
            self.inGame = False

        if x1 > WIDTH - DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > HEIGHT - DOT_SIZE:
            self.inGame = False

    # Puts a new apple at a random point on the canvas and removes the old one.
    def locateApple(self):

        # Locates and delete the eaten apple.
        apple = self.find_withtag("apple")
        self.delete(apple[0])

        # Setting the random X and Y coordinates for new apple.
        r = random.randint(0, RAND_POS)
        self.apple_x = r * DOT_SIZE
        r = random.randint(0, RAND_POS)
        self.apple_y = r * DOT_SIZE

        self.create_image(self.apple_x, self.apple_y, anchor=NW, image=self.apple, tag="apple")

    # Detect the keys pressed.
    def onKeyPressed(self, e):

        key = e.keysym

        if key == "Left" and not self.right:
            self.left = True
            self.up = False
            self.down = False

        if key == "Right" and not self.left:
            self.right = True
            self.up = False
            self.down = False

        if key == "Up" and not self.down:
            self.up = True
            self.right = False
            self.left = False

        if key == "Down" and not self.up:
            self.down = True
            self.right = False
            self.left = False

    # After each DELAY, the onTimer() method is started.
    # The timer is based on the after() method, which only starts
    # the method after DELAY once. To restart the timer, we recursively
    # run the onTimer() method.
    def onTimer(self):

        if self.inGame:
            self.checkCollisions()
            self.checkApple()
            self.doMove()
            self.after(DELAY, self.onTimer)
        else:
            self.gameOver()

    # Delete all object on the canvas and shows the final notice.
    def gameOver(self):

        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text="Ooops, game is over!", fill="black")

# Defines the text in the header of the window and the header itself.
class Snake(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title('Snake!')
        self.board = Board(parent)
        self.pack()


def main():
    root = Tk()
    snake = Snake(root)
    root.mainloop()


if __name__ == '__main__':
    main()