import pygame
import sys

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

# Configuración de teclas del piano
keys = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5"]
black_keys = ["C#4", "D#4", None, "F#4", "G#4", "A#4", None, "C#5", "D#5"]
key_width = WIDTH // len(keys)
black_key_width = key_width // 2
black_key_height = HEIGHT // 2

# Cargar sonidos
sounds = {key: pygame.mixer.Sound(f"{key}.wav") for key in keys + list(filter(None, black_keys))}

# Dibujar teclas del piano
def draw_piano():
    # Dibujar teclas blancas
    for i, key in enumerate(keys):
        rect = pygame.Rect(i * key_width, 0, key_width, HEIGHT)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        font = pygame.font.Font(None, 36)
        text = font.render(key, True, BLACK)
        text_rect = text.get_rect(center=(rect.centerx, rect.centery + 50))
        screen.blit(text, text_rect)

    # Dibujar teclas negras
    for i, key in enumerate(black_keys):
        if key:  # Si hay una tecla negra en esta posición
            rect = pygame.Rect(i * key_width + 3 * key_width // 4, 0, black_key_width, black_key_height)
            pygame.draw.rect(screen, BLACK, rect)

# Reproducir sonido
def play_sound(key):
    if key in sounds:
        sounds[key].play()

# Obtener tecla blanca o negra desde la posición del mouse
def get_key_from_position(x, y):
    # Verificar teclas negras primero
    for i, key in enumerate(black_keys):
        if key:
            rect = pygame.Rect(i * key_width + 3 * key_width // 4, 0, black_key_width, black_key_height)
            if rect.collidepoint(x, y):
                return key
    # Si no es negra, verificar teclas blancas
    key_index = x // key_width
    if 0 <= key_index < len(keys):
        return keys[key_index]
    return None

# Bucle principal
if __name__ == "__main__":
    running = True
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
                if event.key in key_mapping:
                    play_sound(key_mapping[event.key])

        pygame.display.flip()

    pygame.quit()
sys.exit()