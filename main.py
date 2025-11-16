from pygame import init, K_LEFT, K_w, K_ESCAPE, display, QUIT, draw, K_a, K_UP, Surface, K_d, K_SPACE, SRCALPHA, sprite, \
    KEYDOWN, quit, time, event, K_RIGHT, key, font
import random
import math

from pygame.draw import rect, ellipse
from pygame.sprite import Sprite

init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
CLOUD_COLOR = (240, 248, 255)
PLATFORM_COLOR = (34, 139, 34)
FINGER_COLOR = (255, 200, 180)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fingers_collected = 0
        self.image = Surface((50, 50), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.jump_power = -15
        self.gravity = 0.6
        self.update_sprite()

    def update_sprite(self):
        self.image.fill((0, 0, 0, 0))

        palm_color = (255, 220, 177)
        ellipse(self.image, palm_color, (10, 25, 30, 20))
        rect(self.image, palm_color, (10, 30, 30, 15))

        finger_positions = [
            (15, 15),  # Thumb
            (20, 10),  # Index
            (25, 8),   # Middle
            (30, 10),  # Ring
            (35, 15),  # Pinky
        ]

        for i in range(min(self.fingers_collected, 5)):
            x, y = finger_positions[i]
            if i == 0:  # Thumb
                rect(self.image, FINGER_COLOR, (x - 2, y, 4, 12))
            else:
                rect(self.image, FINGER_COLOR, (x, y, 3, 15))

        ellipse(self.image, BLACK, (10, 25, 30, 20), 2)

    def update(self):
        keys = key.get_pressed()
        self.vel_x = 0
        if keys[K_LEFT] or keys[K_a]:
            self.vel_x = -5
        if keys[K_RIGHT] or keys[K_d]:
            self.vel_x = 5

        self.vel_y += self.gravity

        if self.vel_y > 20:
            self.vel_y = 20

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0

        # Check if fell off screen
        if self.rect.top > SCREEN_HEIGHT:
            return True

        return False

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def collect_finger(self):
        self.fingers_collected += 1
        self.update_sprite()


class Platform(Sprite):
    def __init__(self, x, y, width, platform_type="cloud"):
        super().__init__()
        self.width = width
        self.height = 20
        self.type = platform_type
        self.image = Surface((width, self.height), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.draw_platform()

    def draw_platform(self):
        if self.type == "cloud":
            ellipse(self.image, CLOUD_COLOR, (0, 5, self.width, 15))
            ellipse(self.image, CLOUD_COLOR, (self.width // 4, 0, self.width // 2, 20))
            ellipse(self.image, WHITE, (10, 8, self.width - 20, 10))
            ellipse(self.image, (200, 200, 200), (0, 5, self.width, 15), 2)
        else:
            rect(self.image, PLATFORM_COLOR, (0, 0, self.width, self.height))
            rect(self.image, (20, 100, 20), (0, 0, self.width, self.height), 2)

    def update(self, scroll_speed):
        self.rect.y += scroll_speed


class Finger(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((20, 30), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.float_offset = random.randint(0, 100)
        self.draw_finger()

    def draw_finger(self):
        rect(self.image, FINGER_COLOR, (6, 5, 8, 20))
        ellipse(self.image, FINGER_COLOR, (4, 3, 12, 12))
        rect(self.image, BLACK, (6, 5, 8, 20), 2)
        ellipse(self.image, BLACK, (4, 3, 12, 12), 2)

    def update(self, scroll_speed, game_time):
        self.rect.y += scroll_speed
        self.rect.y += math.sin((game_time + self.float_offset) / 10) * 0.5


class Game:
    def __init__(self):
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display.set_caption("HandMan - Collect the Fingers!")
        self.clock = time.Clock()
        self.font = font.Font(None, 36)
        self.small_font = font.Font(None, 24)
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.platforms = sprite.Group()
        self.fingers = sprite.Group()
        self.all_sprites = sprite.Group()
        self.all_sprites.add(self.player)

        self.scroll_speed = 0
        self.game_time = 0
        self.score = 0
        self.running = True
        self.game_over = False

        for i in range(8):
            x = random.randint(50, SCREEN_WIDTH - 150)
            y = SCREEN_HEIGHT - i * 80 - 50
            width = random.randint(80, 150)
            platform_type = random.choice(["cloud", "cloud", "grass"])
            platform = Platform(x, y, width, platform_type)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

        start_platform = Platform(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 50, 150, "grass")
        self.platforms.add(start_platform)
        self.all_sprites.add(start_platform)

    def spawn_platform(self):
        x = random.randint(50, SCREEN_WIDTH - 150)
        y = -20
        width = random.randint(80, 150)
        platform_type = random.choice(["cloud", "cloud", "grass"])
        platform = Platform(x, y, width, platform_type)
        self.platforms.add(platform)
        self.all_sprites.add(platform)

        if random.random() < 0.4:  # 40% chance
            finger_x = x + width // 2 - 10
            finger_y = y - 35
            finger = Finger(finger_x, finger_y)
            self.fingers.add(finger)
            self.all_sprites.add(finger)

    def handle_events(self):
        for e in event.get():
            if e.type == QUIT:
                self.running = False
            elif e.type == KEYDOWN:
                if e.key in (K_SPACE, K_UP, K_w):
                    if not self.game_over:
                        self.player.jump()
                    else:
                        self.reset_game()
                elif e.key == K_ESCAPE:
                    self.running = False

    def update(self):
        if self.game_over:
            return

        self.game_time += 1

        game_over = self.player.update()
        if game_over:
            self.game_over = True
            return

        self.player.on_ground = False

        if self.player.vel_y > 0:
            for platform in self.platforms:
                if self.player.rect.colliderect(platform.rect):
                    if platform.type == "cloud":
                        if self.player.rect.bottom <= platform.rect.top + 10:
                            self.player.rect.bottom = platform.rect.top
                            self.player.vel_y = 0
                            self.player.on_ground = True
                    elif platform.type == "grass":
                        if self.player.rect.bottom <= platform.rect.bottom:
                            self.player.rect.bottom = platform.rect.top
                            self.player.vel_y = 0
                            self.player.on_ground = True

        for platform in self.platforms:
            if platform.type == "grass" and self.player.rect.colliderect(platform.rect):
                if self.player.vel_y < 0 and self.player.rect.top < platform.rect.bottom:
                    self.player.rect.top = platform.rect.bottom
                    self.player.vel_y = 0

        if self.player.rect.top < SCREEN_HEIGHT // 3:
            scroll = (SCREEN_HEIGHT // 3 - self.player.rect.top) * 0.1
            self.scroll_speed = scroll
            self.player.rect.y += scroll
            self.score += int(scroll)
        else:
            self.scroll_speed = 0

        for platform in self.platforms:
            platform.update(self.scroll_speed)
            if platform.rect.top > SCREEN_HEIGHT:
                platform.kill()

        for finger in self.fingers:
            finger.update(self.scroll_speed, self.game_time)
            if finger.rect.top > SCREEN_HEIGHT:
                finger.kill()
            if finger.rect.colliderect(self.player.rect):
                self.player.collect_finger()
                finger.kill()
                self.score += 100

        if len(self.platforms) < 10:
            if random.random() < 0.1:
                self.spawn_platform()

    def draw(self):
        self.screen.fill(SKY_BLUE)

        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        fingers_text = self.font.render(f"Fingers: {self.player.fingers_collected}", True, ORANGE)
        self.screen.blit(fingers_text, (10, 50))

        controls_text = self.small_font.render("SPACE/UP: Jump | LEFT/RIGHT: Move", True, BLACK)
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))

        if self.game_over:
            overlay = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("GAME OVER!", True, WHITE)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            fingers_collected_text = self.font.render(f"Fingers Collected: {self.player.fingers_collected}", True, ORANGE)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)

            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(fingers_collected_text, (SCREEN_WIDTH//2 - fingers_collected_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))

        display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        quit()


if __name__ == "__main__":
    game = Game()
    game.run()

