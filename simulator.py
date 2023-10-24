
import pygame
import math
import sys
import random
import mysql.connector as sql
import time
pygame.init()

con = sql.connect(host="localhost", user="root", passwd="admin", database="gravity")
cur = con.cursor()
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Planet Simulation")
pygame.mouse.set_visible(False)

WIDTH, HEIGHT = WIN.get_size()

#10**30,275266601726, 15566 for circularorbit 
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
DARK_GREY = (80, 78, 81)
LIGHT_GREY = (200, 200, 200)


FONT = pygame.font.SysFont("comicsans", 16)
headfont = pygame.font.SysFont('arial', 30)
childfont = pygame.font.SysFont('arial', 20)

scale = 250

# SIMULATOR RECTANGLES
menu = (WIDTH - WIDTH // 5, HEIGHT // 24, WIDTH // 6, HEIGHT // 2)  # X, Y, WIDTH, HEIGHT
menur = pygame.Rect(menu[0], menu[1], menu[2], menu[3])
mass = (menu[0] + menu[2] // 6, menu[1] + (menu[3])//6, (menu[2] * 2) // 3, menu[3] // 10)
massr = pygame.Rect(mass[0], mass[1], mass[2], mass[3])
radius = (menu[0] + menu[2] // 6, menu[1] + (menu[3]*2) // 6, (menu[2] * 2) // 3, menu[3] // 10)
radiusr = pygame.Rect(radius[0], radius[1], radius[2], radius[3])
colour = (menu[0] + menu[2] // 6, menu[1] + (menu[3] * 3) // 6, (menu[2] * 2) // 3, menu[3] // 10)
colourr = pygame.Rect(colour[0], colour[1], colour[2], colour[3])
velocity = (menu[0] + menu[2] // 6, menu[1] + (menu[3] * 4) // 6, (menu[2] * 2) // 3, menu[3] // 10)
velr = pygame.Rect(velocity[0], velocity[1], velocity[2], velocity[3])
drop = (menu[0] + menu[2] // 6, menu[1] + (menu[3] * 5) // 6, (menu[2] * 2) // 3, menu[3] // 10)
dropr = pygame.Rect(drop[0], drop[1], drop[2], drop[3])
scal = (menu[0], menu[1] + (menu[3] * 7) // 6, menu[2], menu[3] // 4)
scaler = pygame.Rect(scal[0], scal[1], scal[2], scal[3])
back = (menu[0] + menu[2] // 6, HEIGHT - drop[3] - HEIGHT // 32, (menu[2] * 2) // 3, HEIGHT // 16)
backr = pygame.Rect(back[0], back[1], back[2], back[3])
save = (WIDTH // 64, HEIGHT - drop[3] - HEIGHT // 32, (menu[2] * 2) // 3, HEIGHT // 16)
saver = pygame.Rect(save[0], save[1], save[2], save[3])
check = (menu[0] + menu[2] // 6, back[1] - drop[3] - HEIGHT // 32, (menu[2] * 2) // 3, HEIGHT // 16)
checkr = pygame.Rect(check[0], check[1], check[2], check[3])
slide = (menu[0] + menu[2] // 8, menu[1] + (menu[3] * 31) // 24, 6 * menu[2] // 8, menu[3] // 20)
slidr = pygame.Rect(slide[0], slide[1], slide[2], slide[3])
slider = (menu[0] + menu[2] // 8, menu[1] + (menu[3] * 31) // 24 - (menu[3] // 15 - slide[3]) // 2, menu[2] // 8,
          menu[3] // 15)
sliderr = pygame.Rect(slider[0], slider[1], slider[2], slider[3])

max_slide = slide[0] + slide[2] - slider[2] // 2
min_slide = slider[0]

rectlist = [[massr, 'mass'], [radiusr, 'radius'], [colourr, 'colour'], [velr, 'velocity'], [dropr, 'drop']]
currentobj = {'mass': 'MASS', 'radius': 'RADIUS', 'colour': 'COLOUR', 'velocity': 'VELOCITY', 'drop': 'drop'}


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
        radius = 8
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = scale / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = int(mass) 

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def update_timeframe(self, speed):
        self.TIMESTEP = 3600 * 24 * speed

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            if lines:
                pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if distance/self.AU <= 0.1:
            return self, other
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        collide = None
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            if fy == planet:
                collide = planet
                continue
            total_fx += fx
            total_fy += fy
        if collide is not None:
            return collide

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Exan-Regular.ttf", size)


def getanother_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/thefont.ttf", size)

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

particle1 = ParticlePrinciple()
PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 40)

def sim(mas='MASS', rad='RADIUS', col='COLOUR', vel='VELOCITY'):

    # MENU SURFACE
    pygame.draw.rect(WIN, WHITE, menur, 0, 10)
    head = headfont.render('SIMULATOR', True, DARK_GREY)
    WIN.blit(head, (menu[0] + menu[2] // 2 - head.get_width() // 2, menu[1] + head.get_height() // 2))

    # ELEMENTS
    pygame.draw.rect(WIN, LIGHT_GREY, massr, 0, 10)
    head = childfont.render(mas, True, DARK_GREY)
    WIN.blit(head, (mass[0] + mass[2] // 2 - head.get_width() // 2, mass[1] + head.get_height() // 2))

    pygame.draw.rect(WIN, LIGHT_GREY, radiusr, 0, 10)
    head = childfont.render(rad, True, DARK_GREY)
    WIN.blit(head, (radius[0] + radius[2] // 2 - head.get_width() // 2, radius[1] + head.get_height() // 2))

    pygame.draw.rect(WIN, LIGHT_GREY, colourr, 0, 10)
    head = childfont.render(col, True, DARK_GREY)
    WIN.blit(head, (colour[0] + colour[2] // 2 - head.get_width() // 2, colour[1] + head.get_height() // 2))

    pygame.draw.rect(WIN, LIGHT_GREY, velr, 0, 10)
    head = childfont.render(vel, True, DARK_GREY)
    WIN.blit(head, (velocity[0] + velocity[2] // 2 - head.get_width() // 2, velocity[1] + head.get_height() // 2))

    pygame.draw.rect(WIN, GREEN, dropr, 0, 10)
    head = childfont.render('DROP!', True, BLACK)
    WIN.blit(head, (drop[0] + drop[2] // 2 - head.get_width() // 2, drop[1] + head.get_height() // 2))

    pygame.draw.rect(WIN, WHITE, scaler, 0, 10)
    head = headfont.render('SPEED', True, BLACK)
    WIN.blit(head, (scal[0] + scal[2] // 2 - head.get_width() // 2, scal[1] + head.get_height() // 2))

    pygame.draw.rect(WIN, WHITE, backr, 0, 10)
    head = headfont.render('BACK', True, BLACK)
    WIN.blit(head, (back[0] + back[2] // 2 - head.get_width() // 2, back[1] + head.get_height() // 2))

    pygame.draw.rect(WIN, WHITE, saver, 0, 10)
    head = headfont.render('SAVE', True, BLACK)
    WIN.blit(head, (save[0] + save[2] // 2 - head.get_width() // 2, save[1] + head.get_height() // 2))

def slider_blit(slidr, sliderr):
    pygame.draw.rect(WIN, LIGHT_GREY, slidr, 0, 10)
    pygame.draw.rect(WIN, GREEN, sliderr, 0, 10)


def main():
    global sliderr
    global slider
    global start
    run = True
    clock = pygame.time.Clock()

    planets = []
    bl = []
    l = []
    dropped = []
    active_slide = False
    active_rect = None
    drop_active = False
    active_planet = None
    first = True
    menu = True
    load = False
          
    global lines
    lines = True
    speed = 1
    AU = 149.6e6 * 1000
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        if menu == True:
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
                                                              (WIDTH // 4, HEIGHT // 8)),
                                 pos=(WIDTH // 2, (HEIGHT * 3) // 5),
                                 text_input="PLAY", font=get_font(100), base_color="#d7fcd4", hovering_color="#19ff9f")

            LOAD_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rectn.png"),
                                                                 (WIDTH // 6, HEIGHT // 12)),
                                    pos=(WIDTH // 2, HEIGHT * 3 // 5 - HEIGHT // 6),
                                    text_input="LOAD", font=get_font(35), base_color="#d7fcd4",
                                    hovering_color="#19ff9f")
            QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rectn.png"),
                                                              (WIDTH // 6, HEIGHT // 12)),
                                 pos=(WIDTH // 2, HEIGHT * 3 // 5 + HEIGHT // 6),
                                 text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="#19ff9f")

            WIN.blit(MENU_EMBOSS, MENU_EMBOSS_RECT)
            WIN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, LOAD_BUTTON, QUIT_BUTTON]:
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
                        menu = load = False
                        cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='gravity'")
                        s = cur.fetchall()
                        global n
                        n = 0
                        print(s)
                        for i in s:
                            l = int(i[0][1:])
                            if l >= n:
                                n = l+1
                        cur.execute("create table S00"+str(n)+"(mass varchar(255), radius int, r int, g int, b int, velocity bigint, x int, y int, time int)")
                        con.commit()
                    if LOAD_BUTTON.checkForInput(MENU_MOUSE_POS):
                        load = True
                        menu = False

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            particle1.emit()
            pygame.draw.circle(WIN, pygame.Color('Red'), MENU_MOUSE_POS, 8)
            pygame.display.update()
        elif load == True:
            if first == True:
                cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='gravity'")
                s = cur.fetchall()
                for i in range(len(s)):
                    bl.append(Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"),
                                                                      (WIDTH // 12, HEIGHT // 10)),
                                         pos=(WIDTH * (i// 7 + 1) // 10, (HEIGHT * (i % 7+1)) // 8),
                                         text_input=s[i][0], font=get_font(20), base_color="#d7fcd4",
                                         hovering_color="#19ff9f"))
                first = False
            else:
                MENU_MOUSE_POS = pygame.mouse.get_pos()
                particle1.emit()
                for button in bl:
                    button.changeColor(MENU_MOUSE_POS)
                    button.update(WIN)


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            quit()
                    elif event.type == PARTICLE_EVENT:
                        particle1.add_particles()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for button in bl:
                            if button.checkForInput(MENU_MOUSE_POS):
                                simt = button.text_input
                                n = int(simt[1:])
                                cur.execute('select * from ' + simt)
                                l = cur.fetchall()
                                print(l)
                                load = False
                                first = True

                pygame.display.update()

        else:
            if first == True:
                start = time.time()
                first = False

            x, y = pygame.mouse.get_pos()

            if len(bl) != 0 and len(l) != 0:
                d = time.time() - start
                l0 = l[0]
                print(l0[0])
                if d >= l0[8] - 20:
                    # 0-Mass, 1-Radius, 2-R, 3-G, 4-B, 5-Velocity, 6-x, 7-y, 8-Time
                    new_planet = Planet((l0[6] - WIDTH // 2) / scale * Planet.AU, (l0[7] - HEIGHT // 2) / scale * Planet.AU,
                                        l0[1], tuple((l0[2], l0[3], l0[4])), l0[0])
                    new_planet.y_vel = l0[5]
                    planets.append(new_planet)
                    l.pop(0)

            if active_slide == True:
                x = x - slider[2] // 2
                if x >= max_slide:
                    xpos = max_slide
                elif x <= min_slide:
                    xpos = min_slide
                else:
                    xpos = x
                speed = 2**((((xpos - min_slide) / (max_slide - min_slide))*100 - 50) // 5)
                slider = xpos, slider[1], slider[2], slider[3]
                sliderr = pygame.Rect(slider[0], slider[1], slider[2], slider[3])

            if drop_active:
                if active_planet is None:
                    lx, ly = WIDTH // 2, HEIGHT // 2
                    dist = str(math.hypot(abs(x - WIDTH // 2)*AU/scale, abs(y - HEIGHT // 2)*AU/scale))
                else:
                    lx, ly = abs(body.x*scale/body.AU + WIDTH // 2), abs(body.y*scale/body.AU + HEIGHT // 2)
                    dist = str(math.hypot(abs(x - WIDTH // 2)*AU/scale - abs(body.x), abs(y - HEIGHT // 2)*AU/scale - abs(body.y)))
                pygame.draw.line(WIN, LIGHT_GREY, (lx, ly), (x, y))
                head = headfont.render(dist, True, DARK_GREY)
                WIN.blit(head, ((lx + x)//2, (ly + y)//2))

            if backr.collidepoint(float(x), float(y)):
                head = headfont.render('BACK', True, GREEN)
                WIN.blit(head, (back[0] + back[2] // 2 - head.get_width() // 2, back[1] + head.get_height() // 2))

            if saver.collidepoint(float(x), float(y)):
                head = headfont.render('SAVE', True, GREEN)
                WIN.blit(head, (save[0] + save[2] // 2 - head.get_width() // 2, save[1] + head.get_height() // 2))

            if lines:
                pygame.draw.rect(WIN, GREEN, checkr, 0, 10)
                head = headfont.render('SHOW LINES', True, BLACK)
                WIN.blit(head, (check[0] + check[2] // 2 - head.get_width() // 2, check[1] + head.get_height() // 2))
            else:
                pygame.draw.rect(WIN, LIGHT_GREY, checkr, 0, 10)
                head = headfont.render('SHOW LINES', True, BLACK)
                WIN.blit(head, (check[0] + check[2] // 2 - head.get_width() // 2, check[1] + head.get_height() // 2))

            sim(currentobj['mass'], currentobj['radius'], currentobj['colour'], currentobj['velocity'])
            slider_blit(slidr, sliderr)
            particle1.emit()
            pygame.draw.circle(WIN, pygame.Color('Red'), (x, y), 8)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                    if active_rect:
                        if event.key == pygame.K_BACKSPACE:
                            currentobj[active_rect[1]] = currentobj[active_rect[1]][:-1]
                            if currentobj[active_rect[1]] == '':
                                currentobj[active_rect[1]] = active_rect[1].upper()
                        else:
                            if active_rect[1] == currentobj[active_rect[1]].lower():
                                currentobj[active_rect[1]] = ''
                            currentobj[active_rect[1]] += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if sliderr.collidepoint(float(x), float(y)):
                        active_slide = True
                    elif backr.collidepoint(float(x), float(y)):
                        menu = True
                    elif saver.collidepoint(float(x), float(y)):
                        print(dropped)
                        for i in dropped:
                            print(i)
                            cur.execute("insert into S00"+str(n)+" values ("+i[0]+", "+i[1]+", "+i[2]+", "+i[3]+", "+i[4]+", "+i[5]+", "+i[6]+")")
                            con.commit()
                        menu = True
                    elif checkr.collidepoint(float(x), float(y)):
                        lines = not lines
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    for body in planets:
                        if body.radius >= math.hypot(x - abs(body.x*scale/body.AU + WIDTH // 2), y - abs(body.y*scale/body.AU + HEIGHT // 2)):
                            if active_planet != body:
                                active_planet = body
                            else:
                                active_planet = None
                            break
                    else:
                        active_planet = None
                elif event.type == pygame.MOUSEBUTTONUP:
                    if active_slide == True:
                        active_slide = False
                    for rect in rectlist:
                        if rect[0].collidepoint(float(x), float(y)):
                            if currentobj[rect[1]] == 'drop':
                                drop_active = True
                            active_rect = rect
                            if currentobj[active_rect[1]] == active_rect[1].upper():
                                currentobj[active_rect[1]] = ''
                            break
                        else:
                            if currentobj[rect[1]] == '':
                                currentobj[rect[1]] = rect[1].upper()
                    else:
                        active_rect = None

                        if drop_active:
                            drop_active = False
                            new_planet = Planet((x - WIDTH // 2) / scale * Planet.AU, (y - HEIGHT // 2) / scale * Planet.AU, int(currentobj['radius']), eval(currentobj['colour']), eval(currentobj['mass']))
                            new_planet.y_vel = eval(currentobj['velocity'])
                            planets.append(new_planet)
                            dropped.append(tuple(( str(eval(currentobj['mass'])), str(currentobj['radius']), str(currentobj['colour']), str(currentobj['velocity']), str(x), str(y), str(int(time.time()-start)) )))
                            #print("insert into S00"+str(n)+" values ("+str(eval(currentobj['mass']))+", "+str(currentobj['radius'])+", "+str(currentobj['colour'])+", "+str(currentobj['velocity'])+", "+str(x)+", "+str(y)+", "+str(int(time.time()-start))+")")

                            con.commit()
                elif event.type == PARTICLE_EVENT:
                    particle1.add_particles()

            for planet in planets:
                planet.update_timeframe(speed)
                col = planet.update_position(planets)
                if col is not None:
                    planet.radius = (planet.radius + col.radius) // 2
                    planet.mass = planet.mass + col.mass

                    planet.x_vel = planet.x_vel + col.x_vel
                    planet.y_vel = planet.y_vel + col.y_vel
                    planet.color = (planet.color[0] + col.color[0])//2, (planet.color[1] + col.color[1])//2, (planet.color[2] + col.color[2])//2
                    planets.remove(col)
                planet.draw(WIN)

            sped = FONT.render(str(speed)+'x', True, WHITE)
            WIN.blit(sped, (WIDTH // 100, HEIGHT // 100))
            pygame.display.update()

    pygame.quit()
main()
