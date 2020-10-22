import pygame
import math
import random
import pickle
import os


# pygame stuff

white, black, purple, blue = (
    255, 255, 255), (0, 0, 0), (100, 0, 100), (21, 71, 200)


height, width = 1000, 1000

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

btn_positions = [pos1,pos2,pos3,pos4,pos6,pos7,pos8,pos9]



def FractalTree(branchings, angle, stem_length, shrink_factor, squeeze_x, squeeze_y, start_pos, direction=-math.pi / 2, color=black):
    # default direction means Y pointing up
    angle_x = stem_length * math.cos(direction)
    angle_y = stem_length * math.sin(direction)
    (x, y) = start_pos
    next_position = (x + angle_x * squeeze_x, y + angle_y * squeeze_y)
    pygame.draw.line(screen, color, start_pos, next_position, 2)

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
                self.angle + math.radians(pick_random([-20, -10, 0, 10, 20])),
                self.stem_length *
                (1 + pick_random([-0.1, -0.05, 0, 0.05, 0.1])),
                self.shrink_factor *
                (1 + pick_random([-0.1, -0.05, 0, 0.05, 0.1])),
                self.squeeze_x *
                (1 + pick_random([-0.5, -0.25, 0, 0.5, 0.25])),
                self.squeeze_y *
                (1 + pick_random([-0.2, -0.1, 0, 0.1, 0.2])),
            )
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



# for ch in children:
# print(ch.genome())


class Button():
    def __init__(self, color, x, y, width, height, child, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.child = child

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y -
                                            2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def display_gen(screen, parent):

    children = parent.create_children()

    buttons = [
        Button((0, 255, 0), pos1[0] - 75, pos1[1] +
            20, 150, 50, children[0], 'child 1'),
        Button((0, 255, 0), pos2[0] - 75, pos2[1] +
            20, 150, 50, children[1], 'child 2'),
        Button((0, 255, 0), pos3[0] - 75, pos3[1] +
            20, 150, 50, children[2], 'child 3'),
        Button((0, 255, 0), pos4[0] - 75, pos4[1] +
            20, 150, 50, children[3], 'child 4'),
        Button((0, 255, 0), pos6[0] - 75, pos6[1] +
            20, 150, 50, children[4], 'child 5'),
        Button((0, 255, 0), pos7[0] - 75, pos7[1] +
            20, 150, 50, children[5], 'child 6'),
        Button((0, 255, 0), pos8[0] - 75, pos8[1] +
            20, 150, 50, children[6], 'child 7'),
        Button((0, 255, 0), pos9[0] - 75, pos9[1] +
            20, 150, 50, children[7], 'child 8'),
    ]

    generation = len(parent.ancestors) - 1
    text = txtfont.render(f'generation {generation}', True, purple, white)
    textRect = text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (500, 20)

    running = True
    while running:

        screen.fill(white)

        # draw parent
        parent.draw(start_pos=pos5)

        # draw children
        for child, btnpos in zip(children, btn_positions):
            child.draw(start_pos=btnpos)

        # draw buttons
        for button in buttons:
            button.draw(screen, (0, 0, 0))

        screen.blit(text, textRect)

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.isOver(pos):
                        print(f'selected {button.text}')
                        display_gen(screen, button.child)
                        pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.isOver(pos):
                        button.color = (255, 0, 0)
                    else:
                        button.color = (0, 255, 0)


pygame.init()
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.set_mode((height, width))


parent = Biomorph(
    branchings=0,
    angle=math.radians(30),
    stem_length=50,
    shrink_factor=0.8,
    squeeze_x=1,
    squeeze_y=1,
)

txtfont = pygame.font.Font('freesansbold.ttf', 20)

display_gen(screen, parent)
