#raycaster
import pygame, sys, math, threading, time, random

#setup
pygame.init()
wn = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
score_font = pygame.font.SysFont("calibri", 40, True)
FPS_font = pygame.font.SysFont("calibri", 40, True)
health_font = pygame.font.SysFont("calibri", 40, True)


#Game class
class Game:
    def __init__(self):
        self.FPS = 30
        self.state = "running"
        self.score = 0
        self.gun_sound = pygame.mixer.Sound("gunfire.mp3")
        self.explosion_sound = pygame.mixer.Sound("explosion.wav")
        self.nearest_enemy_distance = 1000
        self.map1 = [['#','#','#','#','#','#','#','#','#','#'],
                     ['#','O','#','O','O','O','O','#','O','#'],
                     ['#','O','O','O','#','#','O','#','O','#'],
                     ['#','O','#','#','#','#','O','#','O','#'],
                     ['#','O','#','O','#','O','O','O','O','#'],
                     ['#','O','#','O','O','#','O','#','#','#'],
                     ['#','O','O','O','#','#','O','O','O','#'],
                     ['#','O','#','O','O','O','O','#','O','#'],
                     ['#','O','#','O','#','O','O','O','O','#'],
                     ['#','#','#','#','#','#','#','#','#','#']]
        
        self.map2 = [['#','#','#','#','#','#','#','#','#','#'],
                     ['#','O','#','O','O','O','O','#','O','#'],
                     ['#','O','#','#','#','#','O','#','O','#'],
                     ['#','O','O','O','O','#','O','#','O','#'],
                     ['#','O','#','#','O','O','O','O','O','#'],
                     ['#','O','#','O','O','#','O','#','#','#'],
                     ['#','O','#','#','#','#','O','O','O','#'],
                     ['#','O','O','O','O','O','O','#','O','#'],
                     ['#','O','#','O','#','#','O','O','O','#'],
                     ['#','#','#','#','#','#','#','#','#','#']]


    #handling game events
    def event_handler(self):
        self.dt = time.time() - self.last_time
        self.last_time = time.time()
        self.dt *= 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.fire()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    mx, my = mouse[0], mouse[1]
                    print(mx, my)
        if player.health == 0:
            self.state = "game over"


    #finding the nearest enemy to the player
    def find_nearest_enemy(self):
        for enemy in enemies:
            a = player.x - enemy.x
            b = player.y - enemy.y
            distance = math.sqrt(a**2 + b**2)
            if distance < self.nearest_enemy_distance:
                self.nearest_enemy_distance = distance
                self.nearest_enemy = enemy
        self.nearest_enemy_distance = 1000
        

    #enemy attacking player
    def enemy_attack(self):
        if self.nearest_enemy.state == "alive": self.nearest_enemy.able_to_fire = True
        adj = player.x - self.nearest_enemy.x
        opp = player.y - self.nearest_enemy.y
        self.nearest_enemy.bullet_angle = math.atan2(opp, adj)
        self.nearest_enemy.bullet_x = self.nearest_enemy.x
        self.nearest_enemy.bullet_y = self.nearest_enemy.y
        timer = threading.Timer(random.uniform(1.5, 3), self.enemy_attack)
        timer.start()
        

    #enemy removed from game
    def enemy_remove(self, enemy):
        enemies.remove(enemy)
        

    #new enemy spawning into a valid location
    def enemy_spawn(self):
        respawned = False
        while respawned != True:
            new_x = random.choice([145, 175, 205, 235, 265, 295, 325, 355, 385])
            new_y = random.choice([145, 175, 205, 235, 265, 295, 325, 355, 385])
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O':
                enemies.append(Enemy(new_x, new_y, random.choice(["v", "h"])))
                respawned = True


    #getting the distance from two objects
    def distance(self, x1, y1, x2, y2):
        a, b = x1 - x2, y1 - y2
        return math.sqrt(a**2 + b**2)
        

    #game animations
    def animate(self):
        player.animate_gun()
        player.move()
        for enemy in enemies:
            enemy.move()


    #updating the color of the player health bar
    def update_health_color(self):
        if player.health <= 20: player.health_color = (255, 40, 40)
        elif player.health <= 40: player.health_color = (255, 125, 0)
        elif player.health <= 60: player.health_color = (255, 255, 0)
        elif player.health <= 100: player.health_color = (0, 255, 0)


    #displaying text to the window
    def display_text(self):
        score_text = score_font.render(f"KILLS: {self.score}", True, (255, 255, 255))
        FPS_text = FPS_font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        health_text = health_font.render(f"Health: {player.health}%", True, (255, 255, 255))
        wn.blit(score_text, (100, 30))
        wn.blit(FPS_text, (320, 30))
        wn.blit(health_text, (530, 30))


    #drawing the ceiling and floor to the window
    def draw_ceiling_and_floor(self):
        x, y, y_step, light_intensity = 100, 250, -1, 0
        for k in range(2):
            for l in range(150):
                pygame.draw.rect(wn, (light_intensity, light_intensity, light_intensity), (x, y, 600, 1))
                light_intensity += 0.4
                y += y_step
            y, y_step, light_intensity = 250, 1, 0

            
    #drawing the map
    def draw_map(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                x, y = 614 + j * 8, 107 + i * 8
                if self.grid[i][j] == '#': pygame.draw.rect(wn, (255, 255, 255), (x, y, 7, 7), border_radius = 2)


    #updating the window      
    def update(self):
        pygame.display.update()
        wn.fill((0, 0, 0))
        clock.tick(self.FPS)


    #rendering all objects to the window
    def render(self):
        self.draw_ceiling_and_floor()
        player.cast_rays()
        player.draw_gun()
        pygame.draw.rect(wn, (0, 0, 0), (100, 0, 600, 100))
        pygame.draw.rect(wn, (0, 0, 0), (100, 400, 600, 100))
        pygame.draw.rect(wn, (0, 0, 0), (612, 100, 85, 88))
        self.draw_map()
        for enemy in enemies:
            if enemy.state == "alive": pygame.draw.circle(wn, (255, 0, 0), (614 + abs(enemy.x - 100) * 8/30, 107 + abs(enemy.y - 100) * 8/30), 2)
            else:
                pygame.draw.line(wn, (255, 0, 0), (614 + abs(enemy.x - 100) * 8 / 30 - 2, 107 + abs(enemy.y - 100) * 8 / 30 - 2), (614 + abs(enemy.x - 100) * 8 / 30 + 2, 107 + abs(enemy.y - 100) * 8 / 30 + 2), 2)
                pygame.draw.line(wn, (255, 0, 0), (614 + abs(enemy.x - 100) * 8 / 30 + 2, 107 + abs(enemy.y - 100) * 8 / 30 - 2), (614 + abs(enemy.x - 100) * 8 / 30 - 2, 107 + abs(enemy.y - 100) * 8 / 30 + 2), 2)
        player.draw_rays()
        if game.nearest_enemy.able_to_fire: pygame.draw.circle(wn, (255, 125, 0), (614 + abs(self.nearest_enemy.bullet_x - 100) * 8 / 30, 107 + abs(self.nearest_enemy.bullet_y - 100) * 8 / 30), 1)
        pygame.draw.rect(wn, (255, 255, 255), (100, 100, 600, 300), 5)
        pygame.draw.line(wn, (255, 255, 255), (400, 240), (400, 260), 2)
        pygame.draw.line(wn, (255, 255, 255), (390, 250), (410, 250), 2)
        pygame.draw.rect(wn, (255, 255, 255), (250, 430, 300, 40), 7)
        pygame.draw.rect(wn, player.health_color, (250 + 7, 430 + 7, player.health * 286 / 100, 40 - 7 * 2))
        pygame.draw.circle(wn, (0, 100, 255), (614 + abs(player.x - 100) * 8 / 30, 107 + abs(player.y - 100) * 8 / 30), 2)
        game.display_text()


#Player class
class Player:
    def __init__(self):
        self.x = 145
        self.y = 145
        self.angle = 270
        self.FOV = 60
        self.HALF_FOV = self.FOV // 2
        self.rays = []
        self.gun_sprites = []
        self.current_sprite = 0.7
        self.health = 100
        self.health_color = (0, 255, 0)
        self.animating = False
        self.pain_sound = pygame.mixer.Sound("pain.wav")


    #adding all gun sprites for the firing animation
    def append_gun_sprites(self):
        self.gun_sprites.append(pygame.image.load("gun1.gif"))
        self.gun_sprites.append(pygame.image.load("gun2.gif"))
        self.gun_sprites.append(pygame.image.load("gun3.gif"))
        self.gun_sprites.append(pygame.image.load("gun4.gif"))
        self.gun_sprites.append(pygame.image.load("gun5.gif"))


    #drawing player gun
    def draw_gun(self):
        try: wn.blit(player.gun_sprites[int(player.current_sprite)], (337, 260))
        except:
            player.current_sprite = 0.7
            player.animating = False
            wn.blit(player.gun_sprites[int(player.current_sprite)], (337, 260))


    #drawing player rays
    def draw_rays(self):
        for ray in self.rays:
            pygame.draw.line(wn, (255, 255, 0), (614 + abs(player.x-100)*8/30, 107 + abs(player.y-100)*8/30), ray, 1)
            i, j = int((ray[1] - 107) // 8),  int((ray[0] - 614) // 8)
            if game.grid[i][j] == "#":
                pygame.draw.rect(wn, (0, 200, 0), (614 + j * 8, 107 + i * 8, 7, 7), border_radius = 2)
        self.rays.clear()


    #regenerating health
    def health_regenerate(self):
        if game.score % 5 == 0 and self.health < 80:
            self.health += 20
            game.update_health_color()
        elif game.score % 5 == 0 and self.health >= 80:
            self.health = 100
            game.update_health_color()
            
            
    #controlling player movement and rotation
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_k]: self.angle += game.dt * 4
        if keys[pygame.K_RIGHT] or keys[pygame.K_l]: self.angle -= game.dt * 4
        if keys[pygame.K_w]:
            new_x = self.x + math.cos(math.radians(self.angle)) * game.dt
            new_y = self.y - math.sin(math.radians(self.angle)) * game.dt
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O': self.x, self.y = new_x, new_y
        if keys[pygame.K_s]:
            new_x = self.x - math.cos(math.radians(self.angle)) * game.dt
            new_y = self.y + math.sin(math.radians(self.angle)) * game.dt
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O': self.x, self.y = new_x, new_y
        if keys[pygame.K_a]:
            new_x = self.x + math.cos(math.radians(self.angle + 90)) * 0.8 * game.dt
            new_y = self.y - math.sin(math.radians(self.angle + 90)) * 0.8 * game.dt
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O': self.x, self.y = new_x, new_y
        if keys[pygame.K_d]:
            new_x = self.x + math.cos(math.radians(self.angle - 90)) * 0.8 * game.dt
            new_y = self.y - math.sin(math.radians(self.angle - 90)) * 0.8 * game.dt
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O': self.x, self.y = new_x, new_y


    #casting rays for the wall, the enemies and the enemy bullets
    def cast_rays(self):
        bar_x = 100
        for ray in range(self.FOV):
            angle, depth = self.angle + self.HALF_FOV - ray, 1
            while True: 
                ray_x = self.x + math.cos(math.radians(angle)) * depth
                ray_y = self.y - math.sin(math.radians(angle)) * depth
                i, j = int((ray_y - 100) // 30),  int((ray_x - 100) // 30)
                self.rays.append((614 + abs(ray_x-100)*8/30, 107 + abs(ray_y-100)*8/30))
                if game.grid[i][j] == '#':
                    ray_distance = game.distance(ray_x, ray_y, self.x, self.y) * math.cos(math.radians(abs(self.angle - angle)))
                    bar_height = (1 / ray_distance) * 4000
                    bar_y = 250 - (bar_height / 2)
                    light_intensity = 100 / ray_distance * 100
                    if light_intensity > 255: light_intensity = 255
                    pygame.draw.rect(wn, (light_intensity, light_intensity, light_intensity), (bar_x, bar_y, 10, bar_height))
                    pygame.draw.rect(wn, (0, 200, 0), (614 + j * 8, 107 + i * 8, 7, 7), border_radius = 2)
                    break
                depth += 1
            bar_x += 10
        bar_x = 100
        for ray in range(self.FOV):
            angle, depth, enemy_spotted = self.angle + self.HALF_FOV - ray, 1, False
            while True: 
                ray_x = self.x + math.cos(math.radians(angle)) * depth * 2
                ray_y = self.y - math.sin(math.radians(angle)) * depth * 2
                i, j = int((ray_y - 100) // 30),  int((ray_x - 100) // 30)
                if game.grid[i][j] == '#': break
                for enemy in enemies:
                    distance = game.distance(enemy.x, enemy.y, ray_x, ray_y)
                    if distance < 2 and distance != 0:
                        enemy_spotted = True
                        a = enemy.x - player.x
                        b = enemy.y - player.y
                        distance = math.sqrt(a**2 + b**2)
                        height =  (1 / distance) * enemy.height * math.cos(math.radians(abs(self.angle - angle)))
                        if enemy.state == "alive": bar_y = 250 - (height / 2)
                        else:
                            h = (1 / distance) * 4000 * math.cos(math.radians(abs(self.angle - angle)))
                            bar_y = 250 + (h / 2)
                        pygame.draw.rect(wn, (255, 0, 0), (bar_x, bar_y, 10, height))
                        break
                if enemy_spotted: break
                depth += 1
            bar_x += 10
        if game.nearest_enemy.able_to_fire:    
            bar_x = 100
            for ray in range(self.FOV):
                angle, depth, bullet_spotted = self.angle + self.HALF_FOV - ray, 1, False
                while True: 
                    ray_x = self.x + math.cos(math.radians(angle)) * depth * 5
                    ray_y = self.y - math.sin(math.radians(angle)) * depth * 5
                    i, j = int((ray_y - 100) // 30),  int((ray_x - 100) // 30)
                    if game.grid[i][j] == '#': break
                    distance = game.distance(game.nearest_enemy.bullet_x, game.nearest_enemy.bullet_y, ray_x, ray_y)
                    if distance < 0.5 and distance != 0:
                        bullet_spotted = True
                        a = game.nearest_enemy.bullet_x - player.x
                        b = game.nearest_enemy.bullet_y - player.y
                        distance = math.sqrt(a**2 + b**2)
                        height =  (1 / distance) * 220 * math.cos(math.radians(abs(self.angle - angle)))
                        bar_y = 250 - (height / 2)
                        pygame.draw.circle(wn, (255, 125, 0), (bar_x, bar_y), height)
                        break
                    depth += 1
                if bullet_spotted: break
                bar_x += 10


    #player firing their gun
    def fire(self):
        if self.animating == False:
            game.gun_sound.play()
            game.explosion_sound.play()
            self.animating, enemy_dead = True, False
            depth = 1
            while True:
                ray_x = self.x + math.cos(math.radians(self.angle)) * depth / 2
                ray_y = self.y - math.sin(math.radians(self.angle)) * depth / 2
                for enemy in enemies:
                    distance = game.distance(enemy.x, enemy.y, ray_x, ray_y)
                    if distance < 2 and distance != 0 and enemy.state == "alive":
                        timer = threading.Timer(3, lambda: game.enemy_remove(enemy))
                        timer.start()
                        enemy.state, enemy_dead, enemy.height, enemy.dy, enemy.dx = "dead", True, 500, 0, 0
                        game.enemy_spawn()
                        game.score += 1
                        self.health_regenerate()
                        break
                if enemy_dead: break
                i, j = int((ray_y - 100) // 30),  int((ray_x - 100) // 30)
                try:
                    if game.grid[i][j] == '#': break
                    depth += 1
                except: break
                

    #animating the gun
    def animate_gun(self):
        if self.animating: self.current_sprite += 0.5 * game.dt 



#Enemy class
class Enemy:
    def __init__(self, x, y, movement_direction):
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1
        self.movement_direction = movement_direction
        self.sprites = []
        self.height = 4000
        self.state = "alive"
        self.bullet_x = 0
        self.bullet_y = 0
        self.able_to_fire = False


    #controlling enemy movement
    def move(self):
        distance = game.distance(player.x, player.y, self.x, self.y)
        if distance < 80 and distance != 0 and self.state == "alive":
            angle = math.atan2(player.y - self.y, player.x - self.x)
            new_x = self.x + math.cos(angle) / 2 * game.dt
            new_y = self.y + math.sin(angle) / 2 * game.dt
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O': self.x, self.y = new_x, new_y
        elif self.movement_direction == "v":
            new_x = self.x
            new_y = self.y + self.dy * game.dt * 2
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O': self.x, self.y = new_x, new_y
            elif game.grid[i][j] == '#': self.dy *= -1
        elif self.movement_direction == "h":
            new_x = self.x + self.dx * game.dt * 2
            new_y = self.y
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            if game.grid[i][j] == 'O': self.x, self.y = new_x, new_y
            elif game.grid[i][j] == '#': self.dx *= -1


    #enemy bullet travel
    def bullet_travel(self):
        if self.able_to_fire:
            new_x = self.bullet_x + math.cos(self.bullet_angle) * game.dt * 4
            new_y = self.bullet_y + math.sin(self.bullet_angle) * game.dt * 4
            i, j = int((new_y - 100) // 30),  int((new_x - 100) // 30)
            distance = game.distance(self.bullet_x, self.bullet_y, player.x, player.y)
            if distance < 3 and distance != 0:
                self.able_to_fire = False
                player.pain_sound.play()
                player.health -= 20
                game.update_health_color()
            elif game.grid[i][j] == 'O': self.bullet_x, self.bullet_y = new_x, new_y
            elif game.grid[i][j] == '#': self.able_to_fire = False
            


#creating class instances
game, player = Game(), Player()
player.append_gun_sprites()
game.grid = game.map2
enemies = [Enemy(140, 215, "h"), Enemy(300, 140, "h"), Enemy(360, 320, "v"), Enemy(270, 350, "h"), Enemy(355, 140, "v"), Enemy(265, 235, "h")]
game.last_time = time.time()
game.find_nearest_enemy()
timer = threading.Timer(random.uniform(1.5, 3), game.enemy_attack)
timer.start()

        
#main game loop
while game.state == "running":
    game.event_handler()
    game.animate()
    game.find_nearest_enemy()
    game.nearest_enemy.bullet_travel()
    game.render()
    game.update()


#ending the program
time.sleep(3)
pygame.quit()
