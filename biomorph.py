import pygame
import math
import random
import pickle
import os


# pygame stuff

white, black, purple, blue = (
    255, 255, 255), (0, 0, 0), (100, 0, 100), (21, 71, 200)


height, width = 1000, 1000
pygame.init()
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.set_mode((height, width))

# grid locations
shift = height / 12
pos1 = (width / 6, height / 6 + shift)
pos2 = (width / 2, height / 6 + shift)
pos3 = (5 * width / 6, height / 6 + shift)
pos4 = (width / 6, height / 2 + shift)
pos5 = (width / 2, height / 2 + shift)
pos6 = (5 * width / 6, height / 2 + shift)
pos7 = (width / 6, 5 * height / 6 + shift)
pos8 = (width / 2, 5 * height / 6 + shift)
pos9 = (5 * width / 6, 5 * height / 6 + shift)


def FractalTree(branchings, angle, stem_length, shrink_factor, squeeze_x, squeeze_y, start_pos, direction=-math.pi / 2, color=black):
    # default direction means Y pointing up
    angle_x = stem_length * math.cos(direction)
    angle_y = stem_length * math.sin(direction)
    (x, y) = start_pos
    next_position = (x + angle_x * squeeze_x, y + angle_y * squeeze_y)
    pygame.draw.line(screen, color, start_pos, next_position, 5)

    if branchings > 0:
        new = stem_length * shrink_factor
        FractalTree(branchings - 1, angle, new, shrink_factor, squeeze_x, squeeze_y, next_position,
                    direction - angle, color)
        FractalTree(branchings - 1, angle, new, shrink_factor, squeeze_x, squeeze_y, next_position,
                    direction + angle, color)


def pick_random(lst):
    return(lst[random.randrange(len(lst))])


class Biomorph:
    generation = 0
    name = "LUCA"
    ancestors = []

    def __init__(self, branchings, angle, stem_length, shrink_factor, squeeze_x, squeeze_y):
        self.branchings = branchings
        self.angle = angle
        self.stem_length = stem_length
        self.shrink_factor = shrink_factor
        self.squeeze_x = squeeze_x
        self.squeeze_y = squeeze_y

    def __str__(self):
        return(self.name)

    def __repr__(self):
        return(self.name)

    def genome(self):
        return(vars(self))

    def create_children(self, n=8, save=False):
        children = []
        for child in range(n):
            mutant = Biomorph(
                self.branchings + pick_random([-1, 0, 0, 0, +1]),
                # + math.radians(pick_random([-20, -10, 0, 10, 20])),
                self.angle,
                self.stem_length *
                (1 + pick_random([-0.1, -0.05, 0, 0.05, 0.1])),
                self.shrink_factor *
                (1 + pick_random([-0.1, -0.05, 0, 0.05, 0.1])),
                self.squeeze_x *
                (1 + pick_random([-0.5, -0.25, 0, 0.5, 0.25])),
                self.squeeze_y *
                (1 + pick_random([-0.2, -0.1, 0, 0.1, 0.2])),
            )
            print("TEST")
            print(self.angle)
            mutant.generation = self.generation + 1
            mutant.name = f'gen{mutant.generation}_ch{child+1}'
            if child == 0:
                mutant.ancestors.append(self)
            children.append(mutant)
            if save:
                filename = f'{mutant.name}.pkl'
                fp = os.path.join('biomorphs', filename)
                print(fp)
                #pickle.dump(mutant, open(fp, "wb"))
        return(children)

    def draw(self, start_pos):
        branchings = self.branchings
        angle = self.angle
        stem_length = self.stem_length
        shrink_factor = self.shrink_factor
        squeeze_x = self.squeeze_x
        squeeze_y = self.squeeze_y
        FractalTree(branchings, angle, stem_length, shrink_factor,
                    squeeze_x, squeeze_y, start_pos=start_pos)


parent = Biomorph(
    branchings=3,
    angle=math.radians(30),
    stem_length=50,
    shrink_factor=0.8,
    squeeze_x=1,
    squeeze_y=1,
)


children = parent.create_children()

for ch in children:
    print(ch.genome())

running = True
while running:

    screen.fill(white)

    children[0].draw(start_pos=pos1)
    children[1].draw(start_pos=pos2)
    children[2].draw(start_pos=pos3)
    children[3].draw(start_pos=pos4)
    parent.draw(start_pos=pos5)
    children[4].draw(start_pos=pos6)
    children[5].draw(start_pos=pos7)
    children[6].draw(start_pos=pos8)
    children[7].draw(start_pos=pos9)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
