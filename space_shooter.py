import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.lives = 3
        self.shield = False
        self.shield_timer = 0
        self.rapid_fire = False
        self.rapid_fire_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

        # Update timers
        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False
        if self.rapid_fire:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire = False

    def shoot(self):
        if self.rapid_fire:
            return Bullet(self.rect.centerx, self.rect.top)
        else:
            return Bullet(self.rect.centerx, self.rect.top)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)
        self.shoot_timer = random.randint(60, 120)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(60, 120)
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None

# Enemy Bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        if type == 'life':
            self.image.fill(GREEN)
        elif type == 'rapid':
            self.image.fill(YELLOW)
        elif type == 'shield':
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Star class for background
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Create stars
        for _ in range(100):
            star = Star()
            self.all_sprites.add(star)
            self.stars.add(star)

        self.score = 0
        self.enemy_spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.game_over = False

    def update(self):
        if not self.game_over:
            self.all_sprites.update()

            # Update bullets
            for bullet in self.bullets:
                bullet.update()

            # Update enemies and get their bullets
            for enemy in self.enemies:
                enemy_bullet = enemy.update()
                if enemy_bullet:
                    self.all_sprites.add(enemy_bullet)
                    self.enemy_bullets.add(enemy_bullet)

            # Update enemy bullets
            for bullet in self.enemy_bullets:
                bullet.update()

            # Update powerups
            for powerup in self.powerups:
                powerup.update()

            # Spawn enemies
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= 60:
                self.enemy_spawn_timer = 0
                enemy = Enemy()
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

            # Spawn powerups
            self.powerup_spawn_timer += 1
            if self.powerup_spawn_timer >= 300:
                self.powerup_spawn_timer = 0
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(-100, -40)
                type = random.choice(['life', 'rapid', 'shield'])
                powerup = PowerUp(x, y, type)
                self.all_sprites.add(powerup)
                self.powerups.add(powerup)

            # Check collisions
            # Player bullets hit enemies
            hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
            for hit in hits:
                self.score += 10

            # Enemy bullets hit player
            if not self.player.shield:
                hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
                if hits:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self.game_over = True

            # Enemies hit player
            if not self.player.shield:
                hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if hits:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self.game_over = True

            # Player collects powerups
            hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for hit in hits:
                if hit.type == 'life':
                    self.player.lives += 1
                    self.score += 5
                elif hit.type == 'rapid':
                    self.player.rapid_fire = True
                    self.player.rapid_fire_timer = 300  # 5 seconds
                    self.score += 5
                elif hit.type == 'shield':
                    self.player.shield = True
                    self.player.shield_timer = 300  # 5 seconds
                    self.score += 5

    def draw(self):
        screen.fill(BLACK)
        self.all_sprites.draw(screen)
        self.bullets.draw(screen)
        self.enemy_bullets.draw(screen)
        self.powerups.draw(screen)

        # Draw UI
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))

        if self.player.shield:
            shield_text = font.render("Shield Active", True, BLUE)
            screen.blit(shield_text, (SCREEN_WIDTH - 150, 10))

        if self.player.rapid_fire:
            rapid_text = font.render("Rapid Fire", True, YELLOW)
            screen.blit(rapid_text, (SCREEN_WIDTH - 150, 50))

        if self.game_over:
            game_over_text = large_font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    bullet = self.player.shoot()
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
        return True

# Main game loop
def main():
    game = Game()
    running = True
    while running:
        clock.tick(FPS)
        running = game.handle_events()
        game.update()
        game.draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
