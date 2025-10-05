import pygame
import sys

pygame.init()

# --- Ekran ayarları ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capybara Orchestra")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

# --- Renkler ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- Oyun değişkenleri ---
notes = 0
nota_artis = 1
flute_clicked = False

# --- Görseller ---
background_img = pygame.image.load("images/scane.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

flute_img = pygame.image.load("images/characters/flute.png").convert_alpha()
flute1_img = pygame.image.load("images/characters/flute1.png").convert_alpha()
flute_img = pygame.transform.scale(flute_img, (200, 150))
flute1_img = pygame.transform.scale(flute1_img, (200, 150))
button_rect = flute_img.get_rect(center=(WIDTH // 2, HEIGHT // 1.4))

# --- Müzik ---
pygame.mixer.music.load("music/flute.mp3")
pygame.mixer.music.set_volume(0.8)

music_pos = 0.0
music_length = 20.0
music_playing = False

# --- Ana döngü ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                notes += nota_artis
                flute_clicked = True
                if not music_playing:
                    pygame.mixer.music.play(start=music_pos)
                    music_playing = True
                pygame.time.set_timer(pygame.USEREVENT, 0)

        elif event.type == pygame.MOUSEBUTTONUP:
            flute_clicked = False
            pygame.time.set_timer(pygame.USEREVENT, 1000)

        elif event.type == pygame.USEREVENT:
            pygame.mixer.music.stop()
            music_pos += pygame.mixer.music.get_pos() / 1000.0
            if music_pos >= music_length:
                music_pos = 0.0
            music_playing = False
            pygame.time.set_timer(pygame.USEREVENT, 0)

    # --- Arka planı çiz ---
    screen.blit(background_img, (0, 0))

    # --- Görseller ---
    if flute_clicked:
        screen.blit(flute1_img, button_rect)
    else:
        screen.blit(flute_img, button_rect)

    # --- Nota sayısı ---
    nota_text = font.render(f"Notes: {notes}", True, WHITE)
    screen.blit(nota_text, (30, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()