import pygame
import math
import random

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

#squeeze_x, squeeze_y, shrink_factor


def FractalTree(branchings, angle, stem_length, shrink_factor, squeeze_x, squeeze_y, start_pos=pos1, direction=-math.pi / 2, color=black):
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


# parent genome
par = {
    "branchings": 3,
    "angle": math.radians(30),
    "stem_length": 50,
    "shrink_factor": 0.8,
    "squeeze_x": 1,
    "squeeze_y": 1,
}


def draw_biomorph(genome, pos):
    branchings = genome["branchings"]
    angle = genome["angle"]
    stem_length = genome["stem_length"]
    shrink_factor = genome["shrink_factor"]
    squeeze_x = genome["squeeze_x"]
    squeeze_y = genome["squeeze_y"]
    FractalTree(branchings, angle, stem_length, shrink_factor,
                squeeze_x, squeeze_y, start_pos=pos)


def mutate(genome):
    mutated_genome = {
        # 10% bigger or larger
        "stem_length": genome["stem_length"] * (1 + [-0.5, -0.25, 0, 0.25, 0.5][random.randrange(5)]),
        # 20 deg more or less
        "angle": genome["angle"] + math.radians([-20, -10, 0, 10, 20][random.randrange(5)]),
        "squeeze_x": genome["squeeze_x"] * (1 + [-0.5, -0.25, 0, 0.25, 0.5][random.randrange(5)]),
        "squeeze_y": genome["squeeze_y"] * (1 + [-0.5, -0.25, 0, 0.25, 0.5][random.randrange(5)]),
        "shrink_factor": genome["shrink_factor"] * (1 + [-0.5, -0.25, 0, 0.25, 0.5][random.randrange(5)]),
        "branchings": genome["branchings"] + [-1, 0, 0, 0, +1][random.randrange(5)],
    }
    return(mutated_genome)






def propagate(gen):
    children = [mutate(par) for x in range(8)]
    #pickle children of this generation

ch1 = mutate(par)
ch2 = mutate(par)
ch3 = mutate(par)
ch4 = mutate(par)
ch5 = mutate(par)
ch6 = mutate(par)
ch7 = mutate(par)
ch8 = mutate(par)


pickle.dump(ch1, open("ch1.pkl", "wb"))


running = True
while running:

    screen.fill(white)

    draw_biomorph(ch1, pos1)
    draw_biomorph(ch2, pos2)
    draw_biomorph(ch3, pos3)
    draw_biomorph(ch4, pos4)
    draw_biomorph(par, pos5)
    draw_biomorph(ch5, pos6)
    draw_biomorph(ch6, pos7)
    draw_biomorph(ch7, pos8)
    draw_biomorph(ch8, pos9)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
