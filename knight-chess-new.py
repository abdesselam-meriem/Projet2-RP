import pygame
import sys
import random
import time
import math

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

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
GOLD = (255, 215, 0)
DARK_GREEN = (0, 100, 0)
MENU_BG = (30, 30, 60)  # Dark blue background

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Knight's Tour Genetic Algorithm")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont('Arial', 48, bold=True)
button_font = pygame.font.SysFont('Arial', 32)
info_font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Load knight image and remove white background
def load_knight_image():
    try:
        knight_img = pygame.image.load('knight.png')
        # Set white color as transparent (color key)
        knight_img.set_colorkey((255, 255, 255))
        # Convert for better performance
        knight_img = knight_img.convert_alpha()
        # Scale it to fit nicely in a cell
        knight_img = pygame.transform.scale(knight_img, (CELL_SIZE - 10, CELL_SIZE - 10))
        return knight_img
    except:
        print("Knight image 'knight.png' not found in the same folder as the script!")
        # Create a simple placeholder with transparent background
        placeholder = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
        # Draw a simple knight shape
        pygame.draw.rect(placeholder, (100, 100, 200, 255), (5, 5, CELL_SIZE-20, CELL_SIZE-20), border_radius=8)
        pygame.draw.polygon(placeholder, (150, 150, 220, 255), [
            (CELL_SIZE - 15, 10), 
            (CELL_SIZE - 25, CELL_SIZE - 25), 
            (10, CELL_SIZE - 25)
        ])
        return placeholder

# Load background image
def load_background_image():
    try:
        bg_img = pygame.image.load('background.jpg')
        bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return bg_img
    except:
        print("Background image 'background.jpg' not found. Using solid color background.")
        return None

# Load sounds
def load_sounds():
    sounds = {}
    try:
        sounds['click'] = pygame.mixer.Sound('click.wav')
        sounds['move'] = pygame.mixer.Sound('move.wav')
        sounds['success'] = pygame.mixer.Sound('success.wav')
        # Set volume for sounds
        for sound in sounds.values():
            sound.set_volume(0.5)
    except:
        print("Sound files not found. Continuing without sound.")
    return sounds

# Load resources
knight_image = load_knight_image()
background_image = load_background_image()
sounds = load_sounds()

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
    def __init__(self, x, y, width, height, text, color, hover_color, sound_effects=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surf = button_font.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.sound_effects = sound_effects
        self.hover_played = False
    
    def draw(self, surface):
        # Draw button with gradient effect
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=15)
        
        # Add a subtle border
        border_color = (min(self.current_color[0] + 30, 255), 
                       min(self.current_color[1] + 30, 255), 
                       min(self.current_color[2] + 30, 255))
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=15)
        
        # Add a highlight at the top
        highlight = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 5)
        highlight_color = (min(self.current_color[0] + 50, 255), 
                          min(self.current_color[1] + 50, 255), 
                          min(self.current_color[2] + 50, 255))
        pygame.draw.rect(surface, highlight_color, highlight, border_radius=15)
        
        surface.blit(self.text_surf, self.text_rect)
    
    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            if not self.hover_played and self.sound_effects and 'hover' in self.sound_effects:
                self.sound_effects['hover'].play()
                self.hover_played = True
            self.current_color = self.hover_color
            return True
        self.hover_played = False
        self.current_color = self.color
        return False
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                if self.sound_effects and 'click' in self.sound_effects:
                    self.sound_effects['click'].play()
                return True
        return False

def draw_chessboard(offset_x, offset_y, knight_path=None, current_move_index=0):
    # Draw the chessboard
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, 
                            (offset_x + col * CELL_SIZE, 
                             offset_y + row * CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE))
    
    if knight_path and current_move_index < len(knight_path):
        # Draw path lines up to current move
        for i in range(min(current_move_index, len(knight_path) - 1)):
            if i < len(knight_path) - 1:
                start_x = offset_x + knight_path[i][0] * CELL_SIZE + CELL_SIZE // 2
                start_y = offset_y + knight_path[i][1] * CELL_SIZE + CELL_SIZE // 2
                end_x = offset_x + knight_path[i+1][0] * CELL_SIZE + CELL_SIZE // 2
                end_y = offset_y + knight_path[i+1][1] * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(screen, BLUE, (start_x, start_y), (end_x, end_y), 2)
        
        # Draw visited positions (circles)
        for i in range(current_move_index + 1):
            if i < len(knight_path):
                pos = knight_path[i]
                
                # Draw knight at current position, circles for others
                if i == current_move_index:  # Current position - draw knight
                    knight_rect = knight_image.get_rect(center=(
                        offset_x + pos[0] * CELL_SIZE + CELL_SIZE // 2,
                        offset_y + pos[1] * CELL_SIZE + CELL_SIZE // 2
                    ))
                    screen.blit(knight_image, knight_rect)
                else:  # Other positions - draw circles
                    color = GREEN if i == 0 else PURPLE
                    pygame.draw.circle(screen, color, 
                                      (offset_x + pos[0] * CELL_SIZE + CELL_SIZE // 2,
                                       offset_y + pos[1] * CELL_SIZE + CELL_SIZE // 2),
                                      CELL_SIZE // 4)
                
                # Draw move numbers on all positions except current
                if i < current_move_index:
                    move_text = small_font.render(str(i+1), True, WHITE)
                    text_rect = move_text.get_rect(center=(
                        offset_x + pos[0] * CELL_SIZE + CELL_SIZE // 2,
                        offset_y + pos[1] * CELL_SIZE + CELL_SIZE // 2
                    ))
                    screen.blit(move_text, text_rect)

def main_menu():
    # Create a more attractive button
    start_button = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2, 250, 60, 
                         "START TOUR", (50, 150, 50), (100, 200, 100), sounds)
    
    # Create decorative chess pieces (simplified)
    chess_pieces = []
    for i in range(8):
        chess_pieces.append({
            'pos': (random.randint(50, SCREEN_WIDTH-50), random.randint(100, SCREEN_HEIGHT-100)),
            'size': random.randint(20, 40),
            'color': LIGHT_BROWN if i % 2 == 0 else DARK_BROWN,
            'speed': random.uniform(0.5, 2)
        })
    
    # Animation variables
    angle = 0
    last_time = time.time()
    
    while True:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        angle += dt * 30  # Rotate title slowly
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if start_button.is_clicked(mouse_pos, event):
                main()
                return
        
        # Draw background
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(MENU_BG)
            
            # Draw a subtle pattern
            for i in range(0, SCREEN_WIDTH, 40):
                for j in range(0, SCREEN_HEIGHT, 40):
                    if (i + j) % 80 == 0:
                        pygame.draw.rect(screen, (40, 40, 80), (i, j, 20, 20))
        
        # Draw title with rotation effect
        title_text = title_font.render("KNIGHT'S TOUR", True, GOLD)
        
        # Create a rotated version of the title
        rotated_title = pygame.transform.rotate(title_text, math.sin(angle * 0.01) * 2)
        title_rect = rotated_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        
        # Add a shadow effect
        shadow_text = title_font.render("KNIGHT'S TOUR", True, (20, 20, 20))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 3 + 3))
        screen.blit(shadow_text, shadow_rect)
        
        screen.blit(rotated_title, title_rect)
        
        # Draw subtitle
        subtitle_text = info_font.render("Genetic Algorithm Solution", True, GOLD)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw button
        start_button.check_hover(mouse_pos)
        start_button.draw(screen)
        
        # Draw footer
        footer_text = small_font.render("Press START TOUR to find the optimal knight's path", True, WHITE)
        footer_rect = footer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(footer_text, footer_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    population_size = 50
    # Create the initial population
    population = Population(population_size)
    
    best_solution = None
    max_fit = 0
    
    # Play background music or sound if available
    if 'success' in sounds:
        sounds['success'].play()  # Play a sound when starting the algorithm
    
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
    
    back_button = Button(20, 20, 100, 40, "Back", GRAY, (180, 180, 180), sounds)
    replay_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Replay", LIGHT_BLUE, DARK_BLUE, sounds)
    
    animation_speed = 5  # moves per second
    current_move = 0
    last_move_time = 0
    playing = True
    show_pause_text = False
    pause_text_timer = 0
    pause_text_duration = 2  # seconds to show pause text
    
    # Play success sound when solution is found
    if 'success' in sounds:
        sounds['success'].play()
    
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
                if 'move' in sounds:
                    sounds['move'].play()
            
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
                    if 'move' in sounds:
                        sounds['move'].play()
                elif event.key == pygame.K_LEFT:
                    current_move = max(current_move - 1, 0)
                    playing = False  # Pause when manually stepping
                    show_pause_text = True
                    pause_text_timer = current_time
                    if 'move' in sounds:
                        sounds['move'].play()
        
        # Animate moves
        if playing and current_time - last_move_time > 1 / animation_speed:
            if current_move < len(best_solution.path) - 1:
                current_move += 1
                # Play move sound
                if 'move' in sounds and current_move > 0:
                    sounds['move'].play()
            last_move_time = current_time
        
        # Hide pause text after duration
        if show_pause_text and current_time - pause_text_timer > pause_text_duration:
            show_pause_text = False
        
        screen.fill(WHITE)
        
        # Draw chessboard with current animation state
        draw_chessboard(board_offset_x, board_offset_y, best_solution.path, current_move)
        
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