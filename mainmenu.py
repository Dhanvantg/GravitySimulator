import pygame
import sys
import random

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = WIN.get_size()


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(WIN, pygame.Color('White'), particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        radius = 10
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


# Background

star_field_slow = []
star_field_medium = []
star_field_fast = []

for slow_stars in range(50):  # birth those plasma balls, baby
    star_loc_x = random.randrange(0, WIDTH)
    star_loc_y = random.randrange(0, HEIGHT)
    star_field_slow.append([star_loc_x, star_loc_y])  # i love your balls

for medium_stars in range(35):
    star_loc_x = random.randrange(0, WIDTH)
    star_loc_y = random.randrange(0, HEIGHT)
    star_field_medium.append([star_loc_x, star_loc_y])

for fast_stars in range(15):
    star_loc_x = random.randrange(0, WIDTH)
    star_loc_y = random.randrange(0, HEIGHT)
    star_field_fast.append([star_loc_x, star_loc_y])

# define some commonly used colours
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

pygame.init()

pygame.display.set_caption("Menu")

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
particle1 = ParticlePrinciple()

# nyan_surface = pygame.image.load('nyan_cat.png').convert_alpha()
# particle2 = ParticleNyan()

# particle3 = ParticleStar()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 40)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Exan-Regular.ttf", size)


def getanother_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/thefont.ttf", size)


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WIN.fill("#4f5752")

        OPTIONS_TEXT = get_font(45).render("This is the HELP screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    run = True
    while run:

        WIN.fill(BLACK)

        for star in star_field_slow:
            star[1] += 1
            if star[1] > HEIGHT:
                star[0] = random.randrange(0, WIDTH)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(WIN, DARKGREY, star, 3)

        for star in star_field_medium:
            star[1] += 4
            if star[1] > HEIGHT:
                star[0] = random.randrange(0, WIDTH)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(WIN, LIGHTGREY, star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > HEIGHT:
                star[0] = random.randrange(0, WIDTH)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(WIN, YELLOW, star, 1)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = getanother_font(150).render("GRAVITY", True, "#a1320d")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        MENU_EMBOSS = getanother_font(150).render("GRAVITY", True, WHITE)
        MENU_EMBOSS_RECT = MENU_EMBOSS.get_rect(center=(WIDTH // 2 - WIDTH // 256, HEIGHT // 8))

        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"),
                                                          (WIDTH // 4, HEIGHT // 8)), pos=(WIDTH // 2, (HEIGHT*3) // 5),
                             text_input="PLAY", font=get_font(100), base_color="#d7fcd4", hovering_color="#19ff9f")

        OPTIONS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rectn.png"),
                                            (WIDTH // 6, HEIGHT // 12)), pos=(WIDTH // 2, HEIGHT*3 // 5 - HEIGHT // 6),
                                text_input="HELP", font=get_font(35), base_color="#d7fcd4", hovering_color="#19ff9f")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rectn.png"),
                                            (WIDTH // 6, HEIGHT // 12)), pos=(WIDTH // 2, HEIGHT*3 // 5 + HEIGHT // 6),
                             text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="#19ff9f")

        WIN.blit(MENU_EMBOSS, MENU_EMBOSS_RECT)
        WIN.blit(MENU_TEXT, MENU_RECT)


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == PARTICLE_EVENT:
                particle1.add_particles()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        particle1.emit()
        pygame.display.update()
        clock.tick(120)
    print('ran')


main_menu()
'''
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == PARTICLE_EVENT:
			particle1.add_particles()
			#particle3.add_particles()

	
	particle1.emit()
	
	#particle3.emit()
	pygame.display.update()
'''
