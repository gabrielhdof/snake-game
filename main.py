import pygame, sys
import random


class Snake:

    def __init__(self, size):
        
        self.x = 0
        self.y = 0
        self.xDir = 0
        self.yDir = 1
        self.dir = "down"
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = []
        self.coordinates = set()
        for i in range(size):
            bodyBlock = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body.append(bodyBlock)
           

    def increase_size(self):
        bodyBlock = pygame.Rect(self.body[-1].x, self.body[-1].y, BLOCK_SIZE, BLOCK_SIZE)
        self.body.append(bodyBlock)
        
    def check_collision(self):
        if self.head.x not in range(0, W) or self.head.y not in range(0, H):
            return True
        for block in self.body:
            if self.head.x == block.x and self.head.y == block.y:
                return True
        return False
    

    def move(self, dir):
        global canChangeDir
        if dir == "up" and self.dir != "down":
            self.xDir = 0
            self.yDir = -1
            self.dir = dir
        elif dir == "down" and self.dir != "up":
            self.xDir = 0
            self.yDir = 1
            self.dir = dir
        elif dir == "right" and self.dir != "left":
            self.xDir = 1
            self.yDir = 0
            self.dir = dir
        elif dir == "left" and self.dir != "right":
            self.xDir = -1
            self.yDir = 0
            self.dir = dir
        canChangeDir = False
        
    def update(self):
        global canChangeDir
        self.body.append(self.head)
        if (self.body[0].x, self.body[0].y) in self.coordinates:
            self.coordinates.remove((self.body[0].x, self.body[0].y))
        for i in range(len(self.body)-1):
            
            self.body[i].x = self.body[i+1].x
            self.body[i].y = self.body[i+1].y
            self.coordinates.add((self.body[i+1].x, self.body[i+1].y))
        self.head.x += BLOCK_SIZE * self.xDir
        self.head.y += BLOCK_SIZE * self.yDir
        for rect in self.body:
            pygame.draw.rect(screen, "#88c9d1", rect)
        canChangeDir = True
        self.body.pop()
        

    def check_food(self, food):
        if self.head.x == food.x * BLOCK_SIZE and self.head.y == food.y * BLOCK_SIZE:
            return True
        return False
    

class Food:

    def __init__(self, snake):
        self.avaliable = False
        while self.avaliable is False:
            self.x = random.randint(0,W) // BLOCK_SIZE
            self.y = random.randint(0,H) // BLOCK_SIZE
            if (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE) in snake.coordinates:
                continue
            
            break
            
        self.rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    
    def draw(self, snake):
        # print(f"COMIDA NASCIDA {len(snake.body) - INITIAL_SIZE}")
        pygame.draw.rect(screen, "#a8275d", self.rect)


def draw_grid():
    x = W // BLOCK_SIZE
    y = H // BLOCK_SIZE

    for i in range(x):
        pygame.draw.line(screen, "#031c29", (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, H), 1)
    for i in range(y):
        pygame.draw.line(screen, "#031c29", (0, i * BLOCK_SIZE), (W, i * BLOCK_SIZE), 1)

def updateScore(snake):
    score = len(snake.body) - INITIAL_SIZE
    scoreText = main_font.render(f"Score = {score}", False, "#0a6874")
    scoreTextRect = scoreText.get_rect(midtop = (W/2, 10))
    screen.blit(scoreText, scoreTextRect)

W, H = 600, 600
BLOCK_SIZE = 50
INITIAL_SIZE = 2

timeToMove = 0
pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Jogo da cobrinha")
clock = pygame.time.Clock()

main_font = pygame.font.Font(r"font\Pixeltype.ttf", H // 10)

bg_music = pygame.mixer.Sound(r"sounds\bgMusic.wav")
bg_music.set_volume(0.1)
bg_music.play(-1)
food_sound = pygame.mixer.Sound(r"sounds\food.wav")
lost_sound = pygame.mixer.Sound(r"sounds\lost.wav")
lost_sound.set_volume(5)


snake = Snake(INITIAL_SIZE)
food = Food(snake)

canChangeDir = True


"""color pallete:
    dark blue #031c29
    blue #0a6874
    light blue #88c9d1
    light yellow #fbf7d1
    light pink #d96297
    dark pink #a8275d"""

while True:
    screen.fill("#fbf7d1")
    draw_grid()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and canChangeDir:
            if event.key == pygame.K_w :
                snake.move("up")
            elif event.key == pygame.K_s:
                snake.move("down")
            elif event.key == pygame.K_d:
                snake.move("right")
            elif event.key == pygame.K_a:
                snake.move("left")
    
    if snake.check_food(food):
        snake.increase_size()
        food_sound.play()
        food = Food(snake)
    

    snake.update()
    
    if snake.check_collision():
        lost_sound.play()
        snake = Snake(INITIAL_SIZE)
        food = Food(snake)
    food.draw(snake)
    updateScore(snake)
    
    pygame.display.update()
    clock.tick(10)