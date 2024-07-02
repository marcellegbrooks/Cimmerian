import pygame
import sys
import time  # For tracking the timing of key presses

# Initialize Pygame
pygame.init()

# Set up display
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Magic Keyboard')

# Set up constant and preg-game sounds
Correct = pygame.mixer.Sound('records_sounds/Correct.wav')
L0Key = pygame.mixer.Sound('records_sounds/L1Key.wav')

# Function to load sounds
def load_sound(file_path):
    return pygame.mixer.Sound(file_path)

# Function to check level completion
def check_level_completion(pressed_keys, level_sequence):
    if len(pressed_keys) != len(level_sequence):
        return False
    return all(key == level_sequence[i] for i, key in enumerate(pressed_keys))

# Sounds mapping
sounds = {
    pygame.K_a: load_sound('records_sounds/D2.wav'),
    pygame.K_s: load_sound('records_sounds/E2.wav'),
    pygame.K_d: load_sound('records_sounds/F2.wav'),
    pygame.K_f: load_sound('records_sounds/G2.wav'),
    pygame.K_g: load_sound('records_sounds/A2.wav'),
    pygame.K_h: load_sound('records_sounds/B2.wav'),
}

# Define levels and level keys
levels = [
    [[pygame.K_a, pygame.K_d, pygame.K_g], ['records_sounds/L1Key.wav']],  # Level 1 sequence
    [[pygame.K_g, pygame.K_f, pygame.K_d, pygame.K_s], ['records_sounds/L2Key.wav']], # Level 2 sequence
    [[pygame.K_a, pygame.K_d, pygame.K_g, pygame.K_f, pygame.K_d, pygame.K_s, pygame.K_d, pygame.K_f], ['records_sounds/L3Key.wav']],
    [[pygame.K_a, pygame.K_d, pygame.K_g,
       pygame.K_a, pygame.K_d, pygame.K_g,
       pygame.K_f, pygame.K_d, pygame.K_s, pygame.K_d, pygame.K_f,
       pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_d, pygame.K_s,
       pygame.K_a], ['records_sounds/FinalKey.wav']]
]

# Main game loop Setup
current_level = 0

#Define clues
clue = { pygame.K_SPACE: load_sound(levels[current_level][1][0]) }

# Timing threshold in seconds
timing_threshold = 1.0
clues = 3
L0Clue = 1
key_presses = []
last_key_time = time.time()
running = True

while running:

    if L0Clue == 1:
        L0Clue -= 1
        L0Key.play()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                clue[event.key].play()
                clues -= 1
                if clues == 0:
                    running = False

            else:
                current_time = time.time()
                if event.key in sounds:
                    sounds[event.key].play()
                    # Reset sequence if time between presses is too long
                    if current_time - last_key_time > timing_threshold:
                        key_presses = []
                    key_presses.append(event.key)
                    last_key_time = current_time
                    
                    # Check level completion
                    if check_level_completion(key_presses, levels[current_level][0]):
                        print(f"Level {current_level + 1} complete!")
                        current_level += 1
                        clues = 3 # Reset for next level
                        key_presses = []  # Reset for next level

                        pygame.time.wait(200)
                        Correct.play()

                        if current_level >= len(levels):
                            print("All levels complete! Congratulations!")
                            current_level = 0
                            L0Clue = 1

                        else:
                            clue[pygame.K_SPACE] = load_sound(levels[current_level][1][0]) #load clue
                            pygame.time.wait(3500)
                            clue[pygame.K_SPACE].play()

pygame.quit()
sys.exit()