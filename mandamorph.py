import pygame
import math
import random
import pickle
import os


# pygame stuff

white, black, purple, blue = (
    255, 255, 255), (0, 0, 0), (100, 0, 100), (21, 71, 200)


width, height = 1600, 1000

# grid locations
shift = 0
pos1 = (width / 6, height / 6 + shift)
pos2 = (width / 2, height / 6 + shift)
pos3 = (5 * width / 6, height / 6 + shift)
pos4 = (width / 6, height / 2 + shift)
pos5 = (width / 2, height / 2 + shift)
pos6 = (5 * width / 6, height / 2 + shift)
pos7 = (width / 6, 5 * height / 6 + shift)
pos8 = (width / 2, 5 * height / 6 + shift)
pos9 = (5 * width / 6, 5 * height / 6 + shift)

btn_positions = [pos1, pos2, pos3, pos4, pos6, pos7, pos8, pos9]


def draw_ellipse(A, B, width, color, line):
    """
    draws ellipse between two points
    A = start point (x,y)
    B = end point (x,y)
    width in pixel
    color (r,g,b)
    line thickness int, if line=0 fill ellipse
    """
    # point coordinates
    xA, yA = A[0], A[1]
    xB, yB = B[0], B[1]
    # calculate ellipse height, distance between A and B
    AB = math.sqrt((xB - xA)**2 + (yB - yA)**2)

    # difference between corner point coord and ellipse endpoint
    def sp(theta):
        return abs((width / 2 * math.sin(math.radians(theta))))

    def cp(theta):
        return abs((width / 2 * math.cos(math.radians(theta))))

    if xB >= xA and yB < yA:
        # NE quadrant
        theta = math.degrees(math.asin((yA - yB) / AB))
        xP = int(xA - sp(theta))
        yP = int(yB - cp(theta))
    elif xB < xA and yB <= yA:
        # NW
        theta = math.degrees(math.asin((yB - yA) / AB))
        xP = int(xB - sp(theta))
        yP = int(yB - cp(theta))
    elif xB <= xA and yB > yA:
        # SW
        theta = math.degrees(math.asin((yB - yA) / AB))
        xP = int(xB - sp(theta))
        yP = int(yA - cp(theta))
    else:
        # SE
        theta = math.degrees(math.asin((yA - yB) / AB))
        xP = int(xA - sp(theta))
        yP = int(yA - cp(theta))

    # create surface for ellipse
    ellipse_surface = pygame.Surface((AB, width), pygame.SRCALPHA)
    # draw surface onto ellipse
    if width < 2 * line:
        width = 2 * line
    if AB < 2 * line:
        AB = 2 * line
    pygame.draw.ellipse(ellipse_surface, color, (0, 0, AB, width), line)
    # rotate ellipse
    ellipse = pygame.transform.rotate(ellipse_surface, theta)
    # blit ellipse onto screen
    screen.blit(ellipse, (xP, yP))


globalvar = "global test"


def FractalTree(screen, branchings, angles, start_pos, branch_lengths, branch_widths, direction, i, n, origin, color=(0, 0, 0)):
    # global globalvar
    # globalvar = "changed global"
    # print(globalvar)
    radius = branch_lengths[branchings]
    ellipse_width = branch_widths[branchings]
    yangle = angles[branchings]
    # default direction means Y pointing up
    angle_x = radius * math.cos(direction)
    angle_y = radius * math.sin(direction)
    (x, y) = start_pos
    next_position = (x + angle_x, y + angle_y)
    # pygame.draw.line(screen, color, start_pos, next_position, 2)

    ellipse_outline_width = 2

    draw_ellipse(start_pos, next_position, ellipse_width,
                 color, ellipse_outline_width)

    if branchings > 0:
        FractalTree(screen, branchings - 1, angles, next_position,
                    branch_lengths, branch_widths, direction - yangle, i, n, origin)
        FractalTree(screen, branchings - 1, angles, next_position,
                    branch_lengths, branch_widths, direction + yangle, i, n, origin)

    dist = math.sqrt((next_position[0] - origin[0])
                     ** 2 + (next_position[0] - origin[0])**2)
    return(dist)


def draw_fractal_tree(screen, branchings, angles, branch_lengths, branch_widths, start_pos, n, origin):
    pi2 = 2 * math.pi
    figure_radius = 0
    for i in range(0, n):
        direction = i * pi2 / n - math.pi / 2
        dist = FractalTree(screen, branchings, angles,
                           start_pos, branch_lengths, branch_widths, direction, i, n, origin)
        if figure_radius < dist:
            figure_radius = dist

    return(figure_radius)


def pick_random(lst):
    return(lst[random.randrange(len(lst))])


def do_mutate(prob):
    rand = pick_random(range(0, prob))
    if rand == 0:
        return True
    else:
        return False


class Biomorph:
    generation = 0
    name = "LUCA"
    ancestors = []

    def __init__(self, branchings, angles, branch_lengths, branch_widths, symmetry):
        self.branchings = branchings
        self.angles = angles
        self.branch_lengths = branch_lengths
        self.branch_widths = branch_widths
        self.symmetry = symmetry
        self.figure_radius = 0

    def __str__(self):
        return(self.name)

    def __repr__(self):
        return(self.name)

    def genome(self):
        return(vars(self))

    def create_children(self, n=8, save=False):
        children = []
        for child in range(n):

            # limit to 3 branchings
            if self.branchings > 2:
                new_branchings = self.branchings + \
                    pick_random([-1, 0, 0, 0, 0])
            elif self.branchings == 0:
                new_branchings = self.branchings + \
                    pick_random([+1, 0, 0, 0, 0])
            else:
                new_branchings = self.branchings + \
                    pick_random([-1, 0, 0, 0, +1])

            new_angles = []
            for a in self.angles:
                if do_mutate(4):
                    newa = a + math.radians(pick_random([-10, -5, 5, 10, ]))
                    new_angles.append(newa)
                else:
                    new_angles.append(a)

            new_branch_lengths = []
            for b in self.branch_lengths:
                if do_mutate(4):
                    if b >= 100:
                        newb = pick_random([100, 95, 90])
                    else:
                        newb = b + pick_random([-10, -5, 5, 10])
                    if newb <= 2:
                        newb = pick_random([2, 5, 10])
                    new_branch_lengths.append(newb)
                else:
                    new_branch_lengths.append(b)

            new_branch_widths = []
            for w in self.branch_widths:
                if do_mutate(4):
                    if w >= 100:
                        neww = pick_random([100, 95, 90])
                    else:
                        neww = w + pick_random([-10, -5, 5, 10])
                    if neww <= 2:
                        neww = pick_random([2, 5, 10])
                    new_branch_widths.append(neww)
                else:
                    new_branch_widths.append(w)

            if self.symmetry <= 3:
                new_symmetry = self.symmetry + pick_random([0, 0, 0, 0, 0, +1])
            elif self.symmetry >= 11:
                new_symmetry = self.symmetry + pick_random([0, 0, 0, 0, 0, -1])
            else:
                new_symmetry = self.symmetry + \
                    pick_random([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, +1])

            mutant = Biomorph(
                new_branchings,
                new_angles,
                new_branch_lengths,
                new_branch_widths,
                new_symmetry,
            )

            mutant.generation = self.generation + 1
            mutant.name = f'gen{mutant.generation}_ch{child+1}'
            if child == 0:
                mutant.ancestors.append(self)
            children.append(mutant)
            if save:
                filename = f'{mutant.name}.pkl'
                fp = os.path.join('biomorphs', filename)
                # pickle.dump(mutant, open(fp, "wb"))
        return(children)

    def draw(self, start_pos):
        branchings = self.branchings
        angles = self.angles
        branch_lengths = self.branch_lengths
        branch_widths = self.branch_widths
        symmetry = self.symmetry

        figure_radius = draw_fractal_tree(screen, branchings, angles, branch_lengths, branch_widths,
                                          start_pos, symmetry, start_pos)

        self.figure_radius = figure_radius


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
            font = pygame.font.SysFont('comicsans', 20)
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
        Button((0, 255, 0), pos1[0] - 10, pos1[1] +
               130, 20, 20, children[0], str(children[0].figure_radius)),
        Button((0, 255, 0), pos2[0] - 10, pos2[1] +
               130, 20, 20, children[1], '2'),
        Button((0, 255, 0), pos3[0] - 10, pos3[1] +
               130, 20, 20, children[2], '3'),
        Button((0, 255, 0), pos4[0] - 10, pos4[1] +
               130, 20, 20, children[3], '4'),
        Button((0, 255, 0), pos6[0] - 10, pos6[1] +
               130, 20, 20, children[4], '5'),
        Button((0, 255, 0), pos7[0] - 10, pos7[1] +
               130, 20, 20, children[5], '6'),
        Button((0, 255, 0), pos8[0] - 10, pos8[1] +
               130, 20, 20, children[6], '7'),
        Button((0, 255, 0), pos9[0] - 10, pos9[1] +
               130, 20, 20, children[7], '8'),
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
screen = pygame.display.set_mode((width, height))


parent = Biomorph(
    branchings=0,
    angles=[math.radians(40), math.radians(30),
            math.radians(20), math.radians(10)],
    branch_lengths=[20, 30, 40, 50],
    branch_widths=[15, 25, 35, 45],
    symmetry=3
)

txtfont = pygame.font.Font('freesansbold.ttf', 20)

display_gen(screen, parent)
