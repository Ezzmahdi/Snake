# Import necessary libraries
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Define a class for the cube (individual segments of the snake)
class cube(object):
    # Class variables for the grid dimensions
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start  # Position of the cube
        self.dirnx = 1    # Initial movement direction
        self.dirny = 0
        self.color = color  # Color of the cube

    def move(self, dirnx, dirny):
        # Change the direction of movement
        self.dirnx = dirnx
        self.dirny = dirny
        # Update the position based on the new direction
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # Size of each grid cell
        i = self.pos[0]
        j = self.pos[1]

        # Draw a colored rectangle for the cube
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            # Draw eyes on the snake's head
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# Define a class for the snake
class snake(object):
    body = []  # List to store the snake's body segments
    turns = {}  # Dictionary to store turns (change of direction)

    def __init__(self, color, pos):
        self.color = color  # Color of the snake
        self.head = cube(pos)  # Create the snake's head as a cube
        self.body.append(self.head)  # Add the head to the body list
        self.dirnx = 0  # Initial movement direction (horizontal)
        self.dirny = 1  # Initial movement direction (vertical)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()  # Get keys pressed by the player

        if keys[pygame.K_LEFT]:  # If left arrow key is pressed
            self.dirnx = -1  # Set the horizontal movement direction
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_RIGHT]:  # If right arrow key is pressed
            self.dirnx = 1  # Set the horizontal movement direction
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_UP]:  # If up arrow key is pressed
            self.dirnx = 0
            self.dirny = -1  # Set the vertical movement direction
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_DOWN]:  # If down arrow key is pressed
            self.dirnx = 0
            self.dirny = 1  # Set the vertical movement direction
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Handle boundary conditions - wrap around the grid
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        # Reset the snake to its initial state
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        # Add a new cube to the snake's body
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        # Draw the snake's body
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # Draw the head with eyes
            else:
                c.draw(surface)

# Function to draw the grid lines
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        # Draw vertical and horizontal grid lines
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

# Function to redraw the game window
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))  # Fill the window with black color
    s.draw(surface)  # Draw the snake
    snack.draw(surface)  # Draw the snack
    drawGrid(width, rows, surface)  # Draw the grid lines
    pygame.display.update()  # Update the display

# Function to generate a random snack location
def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # Ensure the snack does not spawn on the snake's body
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

# Function to display a message box
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# Main game loop
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))  # Initialize the game window
    s = snake((255, 0, 0), (10, 10))  # Create the snake(color, position)
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # Create the initial snack
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)  # Delay to control game speed
        clock.tick(10)  # Limit frame rate to 10 frames per second
        s.move()  # Move the snake
        if s.body[0].pos == snack.pos:
            s.addCube()  # Increase the snake's length
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # Generate a new snack

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                # Check for collision with itself - game over
                print('Score:', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))  # Reset the game
                break

        redrawWindow(win)  # Redraw the game window

main()  # Start the game
