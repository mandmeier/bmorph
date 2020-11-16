import pygame
import math
import random


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

btn_positions = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]




def mutate(genome, mutation_rate = 10):

    def pick_random(lst):
        return(lst[random.randrange(len(lst))])

    def do_mutate():
        rand = pick_random(range(0, mutation_rate))
        if rand == 0:
            return True
        else:
            return False

    mutated_genome = [gene + pick_random([-1,1]) if do_mutate() else gene for gene in genome]

    ## check for oversize in structural genes
    mutated_genome[0:7] = [9 if gene > 9 else -9 if gene < -9 else gene for gene in mutated_genome[0:7]]

    ## check for  oversize in recursion depth gene
    mutated_genome[8] = 9 if mutated_genome[8] > 9 else 3 if mutated_genome[8] < 3 else mutated_genome[8]

    return(mutated_genome)


genes = [3, 8, -2, 5, 8, 7, 7, 3, 4]


class Biomorph:
    generation = 0
    name = "LUCA"
    ancestors = []

    def __init__(self, genome):

        self.genome = genome

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
                new_branchings,
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


def FractalTree(branchings, angle, stem_length, shrink_factor, squeeze_x, squeeze_y, start_pos, direction=-math.pi / 2, color=black):
    # default direction means Y pointing up
    angle_x = stem_length * math.cos(direction)
    angle_y = stem_length * math.sin(direction)
    (x, y) = start_pos
    next_position = (x + angle_x * squeeze_x, y + angle_y * squeeze_y)

    ellipse_outline_width = 2
    ellipse_width = stem_length / 3
    #draw_ellipse(start_pos, next_position, ellipse_width,
                 #color, ellipse_outline_width)
    pygame.draw.line(screen, color, start_pos, next_position, 2)

    if branchings > 0:
        new = stem_length * shrink_factor
        FractalTree(branchings - 1, angle, new, shrink_factor, squeeze_x, squeeze_y, next_position,
                    direction - angle, color)
        FractalTree(branchings - 1, angle, new, shrink_factor, squeeze_x, squeeze_y, next_position,
                    direction + angle, color)


GENE_MAX_INDEX = 8
genes = [3, 8, -2, 5, 8, 7, 7, 3, 4]


def getXOffsets(genes):
    return([-genes[1], -genes[0], 0, genes[0], genes[1], genes[2], 0, -genes[2]])


def getYOffsets(genes):
    return([genes[5], genes[4], genes[3], genes[4], genes[5], genes[6], genes[7], genes[6]])


def draw_biomorph(pos, depth, geneIndex, color=black):
    (x1, y1) = pos
    x2 = x1 + depth * getXOffsets(genes)[geneIndex]
    y2 = y1 + depth * getYOffsets(genes)[geneIndex]

    new_pos = (x2, y2)

    pygame.draw.line(screen, color, pos, new_pos, 2)

    if depth > 0:
        draw_biomorph(new_pos, depth - 1, (geneIndex +
                                           (GENE_MAX_INDEX - 1)) % GENE_MAX_INDEX, color=black)
        draw_biomorph(new_pos, depth - 1, (geneIndex + 1) %
                      GENE_MAX_INDEX, color=black)


pygame.init()
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.set_mode((1000, 1000))

running = True
while running:

    screen.fill(white)

    #FractalTree(2, math.radians(30), 50, 0.8, 1, 1, pos5)
    #draw_biomorph(pos5, 80, 35, 40, 30, 20, color=black, branchings = 1)
    draw_biomorph(pos5, genes[GENE_MAX_INDEX], 2)
    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
