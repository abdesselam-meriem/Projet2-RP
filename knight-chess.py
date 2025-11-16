import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BOARD_SIZE = 400
CELL_SIZE = BOARD_SIZE // 8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Knight's Tour Genetic Algorithm")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont('Arial', 48, bold=True)
button_font = pygame.font.SysFont('Arial', 32)
info_font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)


class Chromosome:
    def __init__(self, genes=None):
        if genes is None:
            self.genes = [random.randint(0, 7) for _ in range(63)]
        else:
            self.genes = genes.copy()
    
    def crossover(self, partner):
        crossover_point = random.randint(1, len(self.genes) - 1)
        child_genes = self.genes[:crossover_point] + partner.genes[crossover_point:]
        return Chromosome(child_genes)
    
    def mutation(self, mutation_rate=0.05):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(0, 7)


class Knight:
    def __init__(self, chromosome=None):
        self.chromosome = chromosome if chromosome else Chromosome()
        self.position = (0, 0)
        self.path = [self.position]
        self.fitness = 0
        self.cycle_direction = random.choice([1, -1])
    
    def move_forward(self, direction):
        move_coordinates = {
            1: (-1, -2),   # up-right
            2: (-2, -1),   # right-up  
            3: (-2, 1),    # right-down
            4: (-1, 2),    # down-right
            5: (1, 2),     # down-left
            6: (2, 1),     # left-down
            7: (2, -1),    # left-up
            8: (1, -2)     # up-left
        }
        
        dx, dy = move_coordinates[direction]
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        return (new_x, new_y)
    
    def move_backward(self, direction):
        move_coordinates = {
            1: (-1, -2),   # up-right
            2: (-2, -1),   # right-up  
            3: (-2, 1),    # right-down
            4: (-1, 2),    # down-right
            5: (1, 2),     # down-left
            6: (2, 1),     # left-down
            7: (2, -1),    # left-up
            8: (1, -2)     # up-left
        }
        
        dx, dy = move_coordinates[direction]
        new_x = self.position[0] - dx
        new_y = self.position[1] - dy
        return (new_x, new_y)
    
    def check_moves(self):
        self.position = (0, 0)
        self.path = [self.position]
        visited = set([self.position])
        
        for i, move in enumerate(self.chromosome.genes):
            current_move = move + 1
            new_pos = self.move_forward(current_move)
            
            if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8 and 
                new_pos not in visited):
                self.position = new_pos
                self.path.append(self.position)
                visited.add(self.position)
            else:
                valid_move_found = False
                
                if self.cycle_direction == 1:
                    for j in range(1, 8):
                        new_move = ((current_move - 1 + j) % 8) + 1
                        new_pos = self.move_forward(new_move)
                        
                        if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8 and 
                            new_pos not in visited):
                            self.chromosome.genes[i] = new_move - 1
                            self.position = new_pos
                            self.path.append(self.position)
                            visited.add(self.position)
                            valid_move_found = True
                            break
                else:
                    for j in range(1, 8):
                        new_move = ((current_move - 1 - j) % 8) + 1
                        new_pos = self.move_forward(new_move)
                        
                        if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8 and 
                            new_pos not in visited):
                            self.chromosome.genes[i] = new_move - 1
                            self.position = new_pos
                            self.path.append(self.position)
                            visited.add(self.position)
                            valid_move_found = True
                            break
                
                if not valid_move_found:
                    self.path.append(self.position)
    
    def evaluate_fitness(self):
        self.position = (0, 0)
        temp_visited = set([self.position])
        
        for move in self.chromosome.genes:
            current_move = move + 1
            new_pos = self.move_forward(current_move)
            
            if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8 and 
                new_pos not in temp_visited):
                self.position = new_pos
                temp_visited.add(new_pos)
            else:
                break
        
        self.fitness = len(temp_visited)
        return self.fitness


class Population:
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]
    
    def check_population(self):
        for knight in self.knights:
            knight.check_moves()
    
    def evaluate(self):
        max_fitness = 0
        best_knight = None
        
        for knight in self.knights:
            fitness = knight.evaluate_fitness()
            if fitness > max_fitness:
                max_fitness = fitness
                best_knight = knight
        
        return max_fitness, best_knight
    
    def tournament_selection(self, size=3):
        tournament = random.sample(self.knights, size)
        tournament.sort(key=lambda x: x.fitness, reverse=True)
        return tournament[0], tournament[1]
    
    def create_new_generation(self):
        new_knights = []
        
        while len(new_knights) < self.population_size:
            parent1, parent2 = self.tournament_selection()
            
            child1_chromosome = parent1.chromosome.crossover(parent2.chromosome)
            child2_chromosome = parent2.chromosome.crossover(parent1.chromosome)
            
            child1_chromosome.mutation()
            child2_chromosome.mutation()
            
            new_knights.append(Knight(child1_chromosome))
            if len(new_knights) < self.population_size:
                new_knights.append(Knight(child2_chromosome))
        
        self.knights = new_knights
        self.generation += 1


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surf = button_font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        surface.blit(self.text_surf, self.text_rect)
    
    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        self.current_color = self.color
        return False
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


def draw_chessboard(offset_x, offset_y, knight_path=None):
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, 
                            (offset_x + col * CELL_SIZE, 
                             offset_y + row * CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE))
    
    if knight_path:
        for i, pos in enumerate(knight_path):
            if i < len(knight_path) - 1:
                start_x = offset_x + pos[0] * CELL_SIZE + CELL_SIZE // 2
                start_y = offset_y + pos[1] * CELL_SIZE + CELL_SIZE // 2
                end_x = offset_x + knight_path[i+1][0] * CELL_SIZE + CELL_SIZE // 2
                end_y = offset_y + knight_path[i+1][1] * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(screen, BLUE, (start_x, start_y), (end_x, end_y), 2)
        
        for i, pos in enumerate(knight_path):
            color = GREEN if i == 0 else RED if i == len(knight_path) - 1 else PURPLE
            pygame.draw.circle(screen, color, 
                              (offset_x + pos[0] * CELL_SIZE + CELL_SIZE // 2,
                               offset_y + pos[1] * CELL_SIZE + CELL_SIZE // 2),
                              CELL_SIZE // 4)
            
            if i < len(knight_path) - 1:
                move_text = small_font.render(str(i+1), True, WHITE)
                text_rect = move_text.get_rect(center=(
                    offset_x + pos[0] * CELL_SIZE + CELL_SIZE // 2,
                    offset_y + pos[1] * CELL_SIZE + CELL_SIZE // 2
                ))
                screen.blit(move_text, text_rect)


def main_menu():
    title_text = title_font.render("Knight's Tour Genetic Algorithm", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    
    start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, 
                         "Start", GREEN, (100, 255, 100))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if start_button.is_clicked(mouse_pos, event):
                main()
                return
        
        screen.fill(WHITE)
        screen.blit(title_text, title_rect)
        start_button.check_hover(mouse_pos)
        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    population_size = 50
    # Create the initial population
    population = Population(population_size)
    
    best_solution = None
    max_fit = 0
    
    # Run genetic algorithm until solution is found
    while True:
        # Check the validity of the current population
        population.check_population()
        
        # Evaluate the current generation and get the best knight with its fitness value
        max_fit, best_solution = population.evaluate()
        if max_fit == 64:
            break
        
        # Generate the new population
        population.create_new_generation()
    
    # Create the user interface to display the solution
    show_solution_interface(best_solution, population.generation)


def show_solution_interface(best_solution, generations):
    """Display the optimal solution on an interface"""
    board_offset_x = (SCREEN_WIDTH - BOARD_SIZE) // 2
    board_offset_y = (SCREEN_HEIGHT - BOARD_SIZE) // 2 - 50
    
    back_button = Button(20, 20, 100, 40, "Back", GRAY, (180, 180, 180))
    replay_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Replay", LIGHT_BLUE, DARK_BLUE)
    
    animation_speed = 5  # moves per second
    current_move = 0
    last_move_time = 0
    playing = True
    show_pause_text = False
    pause_text_timer = 0
    pause_text_duration = 2  # seconds to show pause text
    
    while True:
        current_time = time.time()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if back_button.is_clicked(mouse_pos, event):
                return
            
            if replay_button.is_clicked(mouse_pos, event):
                current_move = 0
                playing = True
                show_pause_text = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                    if not playing:
                        # Show pause text when pausing
                        show_pause_text = True
                        pause_text_timer = current_time
                    else:
                        # Hide pause text when resuming
                        show_pause_text = False
                elif event.key == pygame.K_RIGHT:
                    current_move = min(current_move + 1, len(best_solution.path) - 1)
                    playing = False  # Pause when manually stepping
                    show_pause_text = True
                    pause_text_timer = current_time
                elif event.key == pygame.K_LEFT:
                    current_move = max(current_move - 1, 0)
                    playing = False  # Pause when manually stepping
                    show_pause_text = True
                    pause_text_timer = current_time
        
        # Animate moves
        if playing and current_time - last_move_time > 1 / animation_speed:
            if current_move < len(best_solution.path) - 1:
                current_move += 1
            last_move_time = current_time
        
        # Hide pause text after duration
        if show_pause_text and current_time - pause_text_timer > pause_text_duration:
            show_pause_text = False
        
        screen.fill(WHITE)
        
        # Draw chessboard with current animation state
        draw_chessboard(board_offset_x, board_offset_y, best_solution.path[:current_move + 1])
        
        # Draw buttons
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        replay_button.check_hover(mouse_pos)
        replay_button.draw(screen)
        
        # Display information
        title_text = title_font.render("Knight's Tour Solution Found!", True, GREEN)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
        
        info_text = info_font.render(f"Generations: {generations} | Moves: {len(best_solution.path)} | Fitness: 64/64", True, BLACK)
        screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, 80))
        
        move_text = info_font.render(f"Current Move: {current_move}/{len(best_solution.path) - 1}", True, BLACK)
        screen.blit(move_text, (SCREEN_WIDTH // 2 - move_text.get_width() // 2, BOARD_SIZE + board_offset_y + 20))
        
        # Show play/pause status
        status_text = info_font.render("Status: " + ("Playing" if playing else "Paused"), 
                                     True, GREEN if playing else RED)
        screen.blit(status_text, (SCREEN_WIDTH // 2 - status_text.get_width() // 2, BOARD_SIZE + board_offset_y + 50))
        
        controls_text = small_font.render("Controls: SPACE = Pause/Play, LEFT/RIGHT = Step through moves", True, BLACK)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, BOARD_SIZE + board_offset_y + 80))
        
        # Show pause text temporarily when pausing
        if show_pause_text:
            pause_surface = pygame.Surface((300, 80), pygame.SRCALPHA)
            pause_surface.fill((0, 0, 0, 180))  # Semi-transparent black
            pygame.draw.rect(pause_surface, WHITE, (5, 5, 290, 70), 2, border_radius=10)
            
            pause_text = title_font.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(150, 40))
            pause_surface.blit(pause_text, text_rect)
            
            screen.blit(pause_surface, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40))
        
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()