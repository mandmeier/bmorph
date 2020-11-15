import pygame
import math


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



GENE_MAX_INDEX = 8;
genes = [3,8,-2,5,8,7,7,3,4]


def getXOffsets(genes):
    return([-genes[1], -genes[0], 0, genes[0], genes[1], genes[2], 0, -genes[2]])

def getYOffsets(genes):
    return([ genes[5], genes[4], genes[3], genes[4], genes[5], genes[6], genes[7], genes[6]])



def draw_biomorph(pos, depth, geneIndex, color=black):
    (x1, y1) = pos
    x2 = x1 + depth * getXOffsets(genes)[geneIndex]
    y2 = y1 + depth * getYOffsets(genes)[geneIndex]

    new_pos = (x2, y2)

    pygame.draw.line(screen, color, pos, new_pos, 2)

    if depth > 0:
        draw_biomorph( new_pos, depth - 1, ( geneIndex + ( GENE_MAX_INDEX - 1) ) % GENE_MAX_INDEX, color=black)
        draw_biomorph( new_pos, depth - 1, ( geneIndex + 1 ) % GENE_MAX_INDEX, color=black)







pygame.init()
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.set_mode((1000, 1000))

running = True
while running:

    screen.fill(white)

    #FractalTree(2, math.radians(30), 50, 0.8, 1, 1, pos5)
    #draw_biomorph(pos5, 80, 35, 40, 30, 20, color=black, branchings = 1)
    draw_biomorph(pos5,genes[ GENE_MAX_INDEX ],2)
    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
