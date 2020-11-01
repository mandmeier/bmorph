import pygame
import math


height, width = 1000, 1000


def flower(width: int, color: tuple, edges: bool=False):
    W, H = width, width
    # create a flower surface with an alpha channel on which to draw
    # the petals
    flower = pygame.Surface((W, H), pygame.SRCALPHA, 32).convert_alpha()
    R = flower.get_rect()
    cx, cy = R.center
    # assuming petal height should be half their width
    petal_size = (width // 2, width // 4)
    pw, ph = petal_size
    radius = pw / 2
    center_radius = width // 10
    center_color = (255 - color[0], 255 - color[1], 255 - color[2])

    def draw_petal(S, x, y, w, h, angle):
        # Create surface for drawing an individual petal
        surface = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
        # Draw the un-rotated petal
        pygame.draw.ellipse(surface, color, (0, 0, w, h), 0)
        if edges:
            pygame.draw.ellipse(surface, (0, 0, 0), (0, 0, w, h), 1)

        # Create a new surface with the petal rotated by angle
        rot_surface = pygame.transform.rotate(surface, angle)
        # Need center of rotated surface to blit (draw) the rotated
        # petal at the given (x, y) coordinate
        rcx, rcy = rot_surface.get_rect().center
        # Draw the center of the rotated petal at (x, y)
        S.blit(rot_surface, (x - rcx, y - rcy))

    # Petals are drawn at diagonals first, then the horizontal petals,
    # then the vertical petals
    angles = [
        45, 135, 225, 315,      # diagonals
        0, 180,                 # horizontal
        90, 270                 # vertical
    ]
    for a in angles:
        # placing petal centers onto circle of radius (petal_width/2)
        x, y = map(int, (
            radius * math.cos(math.radians(a)), radius *
            math.sin(math.radians(a))
        ))
        draw_petal(flower, cx + x, cy + y, pw, ph, -a)
    # draw flower center (don't remember what it's called)
    pygame.draw.circle(flower, center_color, (cx, cx), center_radius)
    if edges:
        pygame.draw.circle(flower, BLACK, (cx, cx), center_radius, 1)

    def draw_flower(S, x, y, flower=flower):
        S.blit(flower, (x - cx, y - cy))
    return draw_flower


def draw_petal(S, x, y, w, h, angle=0, edges=False):
    # Create surface for drawing an individual petal
    surface = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
    # Draw the un-rotated petal
    #pygame.draw.ellipse(surface, (0, 255, 0), (0, 0, w, h), 0)
    if edges:
        pygame.draw.ellipse(surface, (0, 0, 0), (0, 0, w, h), 2)

    # Create a new surface with the petal rotated by angle
    rot_surface = pygame.transform.rotate(surface, angle)
    # Need center of rotated surface to blit (draw) the rotated
    # petal at the given (x, y) coordinate
    rcx, rcy = rot_surface.get_rect().center
    # Draw the center of the rotated petal at (x, y)
    S.blit(rot_surface, (x - rcx, y - rcy))


def draw_fractal_ngon(Surface, color, n, radius, position, direction=math.pi / 2, branchings=2, shrink_factor=0.5):
    pi2 = 2 * math.pi

    tips = [(int(math.cos(i / n * pi2 - direction) * radius + position[0]),
             int(math.sin(i / n * pi2 - direction) * radius + position[1])) for i in range(0, n)]
    # for tip in tips:
    #pygame.draw.line(Surface, color, position, tip, 2)
    #pygame.draw.circle(screen, (255, 0, 0), position, radius, 2)

    pygame.draw.lines(Surface, color, True, tips, 2)

    if branchings > 0:
        new_radius = int(radius * shrink_factor)
        new_direction = direction
        #new_direction = direction + math.pi / n

        for tip in tips:
            draw_ngon(Surface, color, n, new_radius, tip, direction=new_direction,
                      branchings=branchings - 1, shrink_factor=shrink_factor)


def draw_mandala(Surface, color, n, radius, position, direction=math.pi / 2):
    pi2 = 2 * math.pi
    squeeze_h = 1.2
    squeeze_w = 1.5
    shift2 = 0.75
    squeeze_w2 = 2
    squeeze_h2 = 0.25

    tips = [(int(math.cos(i / n * pi2 - direction) * radius + position[0]),
             int(math.sin(i / n * pi2 - direction) * radius + position[1])) for i in range(0, n)]

    petal_tips = [(int(math.cos(i / n * pi2 - direction) * radius * squeeze_h / 2 + position[0]),
                   int(math.sin(i / n * pi2 - direction) * radius * squeeze_h / 2 + position[1])) for i in range(0, n)]

    petal_tips2 = [(int(math.cos(i / n * pi2 - direction) * radius * 0.75 + position[0]),
                    int(math.sin(i / n * pi2 - direction) * radius * 0.75 + position[1])) for i in range(0, n)]

    pygame.draw.circle(screen, (0, 0, 0), position, radius, 2)

    for tip, i in zip(petal_tips, range(0, n)):
        #pygame.draw.line(Surface, color, position, tip, 2)
        draw_petal(screen, tip[0], tip[1], radius * squeeze_w, radius * squeeze_h,
                   i * 720 / n, edges=True)

    for tip, i in zip(petal_tips2, range(0, n)):
        #pygame.draw.line(Surface, color, position, tip, 2)
        draw_petal(screen, tip[0], tip[1], radius * squeeze_w2, radius * squeeze_h2,
                   i * 720 / n, edges=True)

    #pygame.draw.lines(Surface, color, True, tips, 2)


def draw_fractal_mandala(Surface, color, n, radius, position, direction=math.pi / 2, branchings=2, shrink_factor=0.5):
    pi2 = 2 * math.pi
    squeeze_h = 1.2
    squeeze_w = 1.5

    tips = [(int(math.cos(i / n * pi2 - direction) * radius + position[0]),
             int(math.sin(i / n * pi2 - direction) * radius + position[1])) for i in range(0, n)]

    petal_tips = [(int(math.cos(i / n * pi2 - direction) * radius * squeeze_h / 2 + position[0]),
                   int(math.sin(i / n * pi2 - direction) * radius * squeeze_h / 2 + position[1])) for i in range(0, n)]

    #pygame.draw.circle(screen, (0, 0, 0), position, radius, 2)

    for tip, i in zip(petal_tips, range(0, n)):
        #pygame.draw.line(Surface, color, position, tip, 2)
        draw_petal(screen, tip[0], tip[1], radius * squeeze_w, radius * squeeze_h,
                   i * 720 / n, edges=True)


def FractalTree(screen, start_pos, radius, direction, i, n, shrink_factor=0.5, color=(0, 0, 0), branchings=3, yangle=math.radians(30)):
    # default direction means Y pointing up
    angle_x = radius * math.cos(direction)
    angle_y = radius * math.sin(direction)
    (x, y) = start_pos
    next_position = (x + angle_x, y + angle_y)
    #pygame.draw.line(screen, color, start_pos, next_position, 2)

    draw_petal(screen, next_position[0], next_position[1],
               radius, 2 * radius, angle=i * 720 / n, edges=True)

    if branchings > 0:
        new_radius = radius * shrink_factor
        FractalTree(screen, next_position, new_radius, direction - yangle, i, n,
                    branchings=branchings - 1)
        FractalTree(screen, next_position, new_radius, direction + yangle, i, n,
                    branchings=branchings - 1)


def draw_fractal_tree(screen, start_pos, radius, n):
    pi2 = 2 * math.pi
    for i in range(0, n):
        direction = i * pi2 / n - math.pi / 2
        FractalTree(screen, start_pos, radius, direction, i, n)


def fractal_mandala(screen, position, radius, n, shrink_factor=0.5, direction=-math.pi / 2, branchings=2, angle=math.pi / 5):
    # default direction means Y pointing up
    pi2 = 2 * math.pi

    angle_x = radius * math.cos(direction)
    angle_y = radius * math.sin(direction)

    tips = [(int(math.cos(i / n * pi2 - direction) * radius + position[0]),
             int(math.sin(i / n * pi2 - direction) * radius + position[1])) for i in range(0, n)]

    for tip in tips:
        pygame.draw.line(screen, (0, 0, 0), position, tip, 2)

    if branchings > 0:

        for tip in tips:
            next_position = (tip[0] + angle_x, tip[1] + angle_y)
            new_radius = radius * shrink_factor
        fractal_mandala(screen, next_position, new_radius, n,
                        branchings=branchings - 1, direction=direction - angle)
        fractal_mandala(screen, next_position, new_radius, n,
                        branchings=branchings - 1, direction=direction + angle)


def draw_figure():

    running = True
    while running:

        screen.fill((255, 255, 255))

        # draw

        #pygame.draw.circle(screen, (255, 0, 0), (500, 500), 100)

        #draw_ngon(screen, (0, 0, 0), 6, 200, (500, 500))
        #draw_mandala(screen, (0, 0, 0), 6, 200, (500, 500))
        draw_fractal_tree(screen, (500, 500), 100, 6)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


pygame.init()
pygame.display.set_caption("Mandala")
screen = pygame.display.set_mode((height, width))


draw_figure()
