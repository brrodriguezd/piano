import time
import pygame
import sys
import os
import math
from notas import generate_piano_notes

# si no existe crear el directorio notes
if not os.path.exists("./notes/"):
    os.mkdir("./notes/")

# generar los archivos de notas para el piano
generate_piano_notes()

# Variables globales
start_time = 0
RECORDING = False

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Interactivo")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# Nueva clase para el indicador de grabación
class RecordingIndicator:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.base_radius = radius
        self.current_radius = radius
        self.max_radius = radius * 1.3  # Maximum size for pulsing effect
        self.pulse_speed = 2  # Speed of the pulsing animation
        self.start_time = time.time()

    def update(self):
        # Create a pulsing effect using a sine wave
        elapsed_time = time.time() - self.start_time
        pulse = (math.sin(elapsed_time * self.pulse_speed) + 1) / 2  # Values between 0 and 1
        self.current_radius = self.base_radius + (self.max_radius - self.base_radius) * pulse

    def draw(self, screen):
        # Draw the main red circle
        pygame.draw.circle(screen, RED, (self.x, self.y), int(self.current_radius))
        # Draw "REC" text
        font = pygame.font.Font(None, 24)
        text = font.render("REC", True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.base_radius + 25, self.y))
        screen.blit(text, text_rect)

class PianoKey:
    def __init__(self, note, rect, is_black=False):
        self.note = note
        self.rect = rect
        self.is_black = is_black
        self.base_color = BLACK if is_black else WHITE
        self.current_color = self.base_color
        self.play_start_time = 0
        self.is_playing = False
        self.note_duration = 500  # Duration in milliseconds

    def play(self):
        self.play_start_time = time.time()
        self.is_playing = True

    def update(self):
        if not self.is_playing:
            self.current_color = self.base_color
            return

        elapsed_time = (time.time() - self.play_start_time) * 1000  # Convert to milliseconds
        if elapsed_time >= self.note_duration:
            self.is_playing = False
            self.current_color = self.base_color
            return

        # Calculate color transition (0 to 1)
        progress = 1.0 - (elapsed_time / self.note_duration)

        if self.is_black:
            # Brighten black keys
            brightness = int(100 * progress)
            self.current_color = tuple(min(255, c + brightness) for c in self.base_color)
        else:
            # Darken white keys
            darkness = int(150 * progress)
            self.current_color = tuple(max(0, c - darkness) for c in self.base_color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        font = pygame.font.Font(None, 36 if not self.is_black else 24)
        text = font.render(self.note, True, BLACK if not self.is_black else WHITE)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery + 50))
        screen.blit(text, text_rect)

# Configuración de teclas del piano
keys = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5"]
black_keys = ["C#4", "D#4", None, "F#4", "G#4", "A#4", None, "C#5", "D#5"]
key_width = WIDTH // len(keys)
black_key_width = key_width // 2
black_key_height = HEIGHT // 2

# Crear objetos de teclas
white_key_objects = []
black_key_objects = []

# Crear teclas blancas
for i, key in enumerate(keys):
    rect = pygame.Rect(i * key_width, 0, key_width, HEIGHT)
    white_key_objects.append(PianoKey(key, rect, False))

# Crear teclas negras
for i, key in enumerate(black_keys):
    if key:
        rect = pygame.Rect(i * key_width + 3 * key_width // 4, 0, black_key_width, black_key_height)
        black_key_objects.append(PianoKey(key, rect, True))

# Crear indicador de grabación
recording_indicator = RecordingIndicator(30, 30, 10)

# Cargar sonidos
sounds = {key: pygame.mixer.Sound(f"notes/{key}.wav") for key in keys + list(filter(None, black_keys))}

def log_note(note):
    elapsed_time = time.time() - start_time
    with open("notes.txt", "a+") as file:
        file.write(f"{elapsed_time:.2f} - {note}\n")

def draw_piano():
    # Dibujar teclas blancas primero
    for key in white_key_objects:
        key.update()
        key.draw(screen)

    # Dibujar teclas negras encima
    for key in black_key_objects:
        key.update()
        key.draw(screen)

    # Dibujar indicador de grabación si está activo
    if RECORDING:
        recording_indicator.update()
        recording_indicator.draw(screen)

def play_sound(note):
    if RECORDING:
        log_note(note)
    if note in sounds:
        sounds[note].play()
        # Encontrar y animar la tecla correspondiente
        for key in white_key_objects + black_key_objects:
            if key.note == note:
                key.play()
                break

def get_key_from_position(x, y):
    # Verificar teclas negras primero
    for key in black_key_objects:
        if key.rect.collidepoint(x, y):
            return key.note
    # Verificar teclas blancas
    for key in white_key_objects:
        if key.rect.collidepoint(x, y):
            return key.note
    return None

# Bucle principal
if __name__ == "__main__":
    running = True
    RECORDING = False
    while running:
        screen.fill(GRAY)
        draw_piano()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                key = get_key_from_position(x, y)
                if key:
                    play_sound(key)
            elif event.type == pygame.KEYDOWN:
                key_mapping = {
                    pygame.K_a: "C4", pygame.K_w: "C#4", pygame.K_s: "D4", pygame.K_e: "D#4", pygame.K_d: "E4",
                    pygame.K_f: "F4", pygame.K_t: "F#4", pygame.K_g: "G4", pygame.K_y: "G#4", pygame.K_h: "A4",
                    pygame.K_u: "A#4", pygame.K_j: "B4", pygame.K_k: "C5", pygame.K_o: "C#5", pygame.K_l: "D5",
                    pygame.K_p: "D#5"
                }
                if event.key == pygame.K_SPACE:
                    RECORDING = not RECORDING
                    if RECORDING:
                        print("RECORDING")
                        with open("notes.txt", "w") as file:
                            file.write("")
                        start_time = time.time()
                    else:
                        print("NOT RECORDING")

                if event.key in key_mapping:
                    play_sound(key_mapping[event.key])

        pygame.display.flip()

    pygame.quit()
sys.exit()
