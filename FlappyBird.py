import pygame
import os
import random

WIDTH = 400
HEIGHT = 700

IMG_DIR = os.path.join(os.path.dirname(__file__), 'imgs')
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join(IMG_DIR, 'pipe.png')))
FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join(IMG_DIR, 'base.png')))
BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(IMG_DIR, 'bg.png')))
BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(IMG_DIR, 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(IMG_DIR, 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(IMG_DIR, 'bird3.png')))
]

pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 50)

class Bird:
    IMGS = BIRD

    # Rotate animation
    MAX_ROTATE = 25
    SPEED_ROTATE = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_counter = 0
        self.image = self.IMGS[0]
    
    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y
    
    def movement(self):
        # calculate the movement
        self.time += 1
        movement = 1.5 * (self.time**2) + self.speed + self.time

        # restrict movement
        if movement > 16:
            movement = 16
        
        elif movement < 0:
            movement -= 2
        
        self.y = movement

        # bird angle
        if movement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATE:
                self.angle = self.MAX_ROTATE
        else:
            if self.angle > -90:
                self.angle -= self.SPEED_ROTATE
    
    def draw(self, screen):
        # bird image
        self.image_counter += 1

        if self.image_counter < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        
        elif self.image_counter < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]

        elif self.image_counter < self.ANIMATION_TIME*3:
            self.image = self.IMGS[3]

        elif self.image_counter < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        
        elif self.image_counter < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMGS[0]
            self.image_counter = 0

        # check if bird is falling
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image_counter = self.ANIMATION_TIME*2
        
        # draw the image
            rotate_img = pygame.transform.rotate(self.image, self.angle)
            center_position_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
            retangle = rotate_img.get_rect(center=center_position_img)
            screen.blit(rotate_img, retangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pos = 0
        self.base_pos = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE, False, True)
        self.BASE_PIPE = PIPE
        self.passed = False
        self.define_height()

    def define_height(self):
        self.height = random.randrange(50, 450)
        self.top_pos = self.height - self.TOP_PIPE.get_height()
        self.base_pos = self.height + self.DISTANCE
        
    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.TOP_PIPE, (self.x, self.top_pos))
        screen.blit(self.BASE_PIPE, (self.x, self.top_pos))
    
    def colidir(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BASE_PIPE)

        top_distance = (self.x - bird.x, self.top_pos - round(bird.y))
        base_distance = (self.x - bird.x, self.base_pos - round(bird.y))

        point_top = bird_mask.overlap(top_mask, top_distance)
        point_base = bird_mask.overlap(base_mask, base_distance)

        if point_top or point_base:
            return True
        else:
            return False

class Base:
    SPEED = 5
    WIDTH = FLOOR.get_width()
    IMAGE = FLOOR

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))

def draw_screen(screen, birds, pipes, base, score):
    screen.blit(BACKGROUND, (0, 0))  # Draw background first
    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    text = SCORE_FONT.render(f'SCORE: {score}', 1, (255, 255, 255))
    screen.blit(text, (WIDTH - 10 - text.get_width()))
    base.draw(screen)
    pygame.display.update()  # Update display after drawing

def main():
    birds = [Bird(230, 350)]
    floor = Base(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    score = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(50)
        pygame.event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        for bird in birds:
            bird.movement()
        floor.move()

        add_pipe = False
        remove_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colidir(bird):
                    birds.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                remove_pipes.append(pipe)
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
    
    draw_screen(screen, birds, pipes, floor, score)

if __name__ == '__main__':
    main()