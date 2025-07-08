import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
CELL_NUMBER_X = WINDOW_WIDTH // CELL_SIZE
CELL_NUMBER_Y = WINDOW_HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 150, 0)

class Snake:
    def __init__(self):
        self.body = [pygame.Vector2(5, 10), pygame.Vector2(4, 10), pygame.Vector2(3, 10)]
        self.direction = pygame.Vector2(1, 0)
        self.new_block = False
        
    def draw_snake(self, screen):
        for block in self.body:
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, DARK_GREEN, block_rect)
            
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            
    def add_block(self):
        self.new_block = True
        
    def check_collision(self):
        # Check wall collision
        if not 0 <= self.body[0].x < CELL_NUMBER_X or not 0 <= self.body[0].y < CELL_NUMBER_Y:
            return True
            
        # Check self collision
        for block in self.body[1:]:
            if block == self.body[0]:
                return True
                
        return False

class Food:
    def __init__(self):
        self.randomize()
        
    def draw_food(self, screen):
        food_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
        
    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER_X - 1)
        self.y = random.randint(0, CELL_NUMBER_Y - 1)
        self.pos = pygame.Vector2(self.x, self.y)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        
    def draw_elements(self, screen):
        self.draw_grass(screen)
        self.food.draw_food(screen)
        self.snake.draw_snake(screen)
        self.draw_score(screen)
        
    def check_collision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize()
            self.snake.add_block()
            self.score += 1
            
        # Make sure food doesn't spawn on snake
        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.randomize()
                
    def check_fail(self):
        if self.snake.check_collision():
            self.game_over()
            
    def game_over(self):
        pygame.quit()
        sys.exit()
        
    def draw_grass(self, screen):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER_Y):
            if row % 2 == 0:
                for col in range(CELL_NUMBER_X):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER_X):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                        
    def draw_score(self, screen):
        score_text = str(self.score)
        font = pygame.font.Font(None, 36)
        score_surface = font.render(score_text, True, BLACK)
        score_x = int(WINDOW_WIDTH - 60)
        score_y = int(WINDOW_HEIGHT - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

def main():
    # Set up the display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game()
    
    # Custom event for snake movement
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == SCREEN_UPDATE:
                game.update()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if game.snake.direction.y != 1:
                        game.snake.direction = pygame.Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if game.snake.direction.y != -1:
                        game.snake.direction = pygame.Vector2(0, 1)
                if event.key == pygame.K_RIGHT:
                    if game.snake.direction.x != -1:
                        game.snake.direction = pygame.Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    if game.snake.direction.x != 1:
                        game.snake.direction = pygame.Vector2(-1, 0)
        
        screen.fill((175, 215, 70))
        game.draw_elements(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
