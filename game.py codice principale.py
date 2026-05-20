import pygame
import random
import sys
pygame.init()

# Schermo
WIDTH = 1000
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Shooter")

clock = pygame.time.Clock()

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
RED = (200, 50, 50)

# Player
player = pygame.Rect(100, 350, 50, 50)
player_velocity_y = 0
gravity = 1
jump_force = -18
on_ground = True

# Proiettili
bullets = []

# Ostacoli
obstacles = []

# Score
score = 0
font = pygame.font.SysFont(None, 40)

# Timer ostacoli
spawn_timer = 0

running = True

while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Salto
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_velocity_y = jump_force
                on_ground = False

            # Sparo
            if event.key == pygame.K_f:
                bullet = pygame.Rect(
                    player.x + 40,
                    player.y + 20,
                    15,
                    5
                )
                bullets.append(bullet)

    # Gravità
    player_velocity_y += gravity
    player.y += player_velocity_y

    # Pavimento
    if player.y >= 350:
        player.y = 350
        player_velocity_y = 0
        on_ground = True

    # Spawn ostacoli
    spawn_timer += 1

    if spawn_timer > 50:
        spawn_timer = 0

        obstacle_type = random.choice(["ground", "flying"])

        if obstacle_type == "ground":
            obstacle = pygame.Rect(WIDTH, 360, 40, 40)
        else:
            obstacle = pygame.Rect(WIDTH, 250, 50, 30)

        obstacles.append(obstacle)

    # Movimento ostacoli
    for obstacle in obstacles[:]:
        obstacle.x -= 8

        if obstacle.x < -100:
            obstacles.remove(obstacle)
            score += 1

        # Collisione player
        if player.colliderect(obstacle):
            print("GAME OVER")
            pygame.quit()
            sys.exit()

    # Movimento proiettili
    for bullet in bullets[:]:
        bullet.x += 15

        if bullet.x > WIDTH:
            bullets.remove(bullet)

    # Collisioni proiettili
    for bullet in bullets[:]:
        for obstacle in obstacles[:]:

            if bullet.colliderect(obstacle):

                if bullet in bullets:
                    bullets.remove(bullet)

                if obstacle in obstacles:
                    obstacles.remove(obstacle)

                score += 5

    # Disegni
    pygame.draw.rect(screen, GREEN, player)

    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Pavimento
    pygame.draw.line(screen, BLACK, (0, 400), (WIDTH, 400), 3)

    # Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

pygame.quit()
