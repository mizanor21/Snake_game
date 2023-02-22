import pygame
import random

# set up constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# initialize pygame
pygame.init()

# set up game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')


# define classes
class Snake:
    def __init__(self):
        self.positions = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.color = (0, 255, 0)

    def draw(self, surface):
        for position in self.positions:
            x, y = position
            pygame.draw.rect(surface, self.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def turn(self, direction):
        if self.direction != (-direction[0], -direction[1]):
            self.direction = direction

    def move(self):
        x, y = self.positions[0]
        dx, dy = self.direction
        new_position = (x + dx, y + dy)
        if new_position in self.positions[1:] or not (
                0 <= new_position[0] < GRID_WIDTH and 0 <= new_position[1] < GRID_HEIGHT):
            return False
        self.positions.insert(0, new_position)
        self.positions.pop()
        return True


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize_position()

    def draw(self, surface):
        x, y = self.position
        pygame.draw.rect(surface, self.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))


class Obstacle:
    def __init__(self, position):
        self.position = position
        self.color = (255, 255, 255)

    def draw(self, surface):
        x, y = self.position
        pygame.draw.rect(surface, self.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Level:
    def __init__(self, speed, obstacles, food_needed):
        self.speed = speed
        self.obstacles = obstacles
        self.food_needed = food_needed


# define functions
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


# define main function
def main():
    # create snake, food, and obstacles
    snake = Snake()
    food = Food()
    obstacles = [
        Obstacle((7, 7)),
        Obstacle((7, 8)),
        Obstacle((7, 9)),
        Obstacle((7, 10)),
        Obstacle((7, 11))
    ]

    # create levels
    levels = [
        Level(speed=5, obstacles=[], food_needed=5),
        Level(speed=10, obstacles=[], food_needed=10),
        Level(speed=15, obstacles=[], food_needed=15),
        Level(speed=20, obstacles=obstacles, food_needed=20)
    ]
    current_level = 0

    # set up clock and font
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    # set up game loop
    running = True
    game_over = False
    game_won = False
    while running:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

        # move snake
        if not game_over and not game_won:
            if not snake.move():
                game_over = True
            elif snake.positions[0] == food.position:
                snake.positions.append(snake.positions[-1])
                food.randomize_position()
                if len(snake.positions) - 3 == levels[current_level].food_needed:
                    current_level += 1
                    if current_level == len(levels):
                        game_won = True
                        game_over = True

        # draw screen
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        for obstacle in levels[current_level].obstacles:
            obstacle.draw(screen)

        # draw UI
        if game_over:
            if game_won:
                draw_text(screen, 'You Win!', font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 48)
            else:
                draw_text(screen, 'Game Over!', font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 48)
            draw_text(screen, 'Press R to restart', font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            draw_text(screen, f'Level {current_level + 1}', font, WHITE, SCREEN_WIDTH // 2, 32)
            draw_text(screen, f'Food eaten: {len(snake.positions) - 3}/{levels[current_level].food_needed}', font,
                      WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 32)

        # update screen and tick clock
        pygame.display.update()
        clock.tick(levels[current_level].speed)

        # handle restart
        keys = pygame.key.get_pressed()
        if game_over and keys[pygame.K_r]:
            snake = Snake()
            food = Food()
            current_level = 0
            game_over = False
            game_won = False

    # quit pygame
    pygame.quit()


if __name__ == '__main__':
    main()

