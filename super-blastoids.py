import pygame
import math
import random
import signal
import sys
import numpy as np
from flask import Flask, render_template_string
import threading

# Initialize Flask app
app = Flask(__name__)

# HTML template for the game landing page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Super Blastoids</title>
  <style>
    html, body {
      margin: 0;
      height: 100%;
      background: black;
      font-family: 'Arial', sans-serif;
      color: #0f0;
      text-align: center;
    }
    h1 {
      margin-top: 20%;
      font-size: 48px;
    }
    p {
      font-size: 24px;
    }
  </style>
</head>
<body>
  <h1>Super Blastoids</h1>
  <p>The game is running locally. Use <b>W/S</b> to speed up/down, <b>A/D</b> to move left/right, <b>R/F</b> to move up/down, <b>Q/E</b> to rotate left/right, <b>SPACE</b> to fire flares.</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

def handle_sigint(sig, frame):
    pygame.quit()
    sys.exit(0)

# Sound utility: create a simple sine wave sound using numpy and pygame.sndarray
def sine_sound(frequency=440, duration=0.2, volume=0.5, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    buffer = (np.sin(2 * np.pi * np.arange(n_samples) * frequency / sample_rate) * 32767 * volume).astype(np.int16)
    if buffer.ndim == 1:
        # Duplicate for stereo
        buffer = np.column_stack([buffer, buffer])
    sound = pygame.sndarray.make_sound(buffer)
    return sound

# Pygame game logic
def run_game():
    pygame.init()
    # For mixer: ensure it's initialized before generating sounds
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.display.init()
    pygame.mixer.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Super Blastoids")

    # Colors
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)

    # Ship properties (first-person perspective)
    ship = {
        'x': 0,  # Lateral position within tunnel (-1 to 1)
        'y': 0,  # Vertical position within tunnel (-1 to 1)
        'speed': 0.05,
        'rotation': 0,  # Added: rotation (radians)
    }

    # Tunnel properties
    tunnel_segments = []
    tunnel_depth = 10  # Number of segments for depth
    tunnel_speed = 0.1
    tunnel_width = 2  # Tunnel width in normalized units
    tunnel_height = 2  # Tunnel height in normalized units

    # Game objects
    asteroids = []
    flares = []

    # Sine sounds for actions
    SND_FIRE = sine_sound(620, 0.08, 0.3)
    SND_HIT = sine_sound(180, 0.12, 0.5)
    SND_MOVE = sine_sound(370, 0.05, 0.15)
    SND_SPEEDUP = sine_sound(800, 0.05, 0.3)
    SND_SLOWDOWN = sine_sound(220, 0.07, 0.3)
    SND_ROTATE = sine_sound(380, 0.04, 0.06)

    class Asteroid:
        def __init__(self):
            self.z = tunnel_depth  # Depth position
            self.x = random.uniform(-tunnel_width / 2, tunnel_width / 2)
            self.y = random.uniform(-tunnel_height / 2, tunnel_height / 2)
            self.radius = random.uniform(0.1, 0.3)
            self.speed = random.uniform(0.05, 0.15)

        def update(self):
            self.z -= self.speed
            if self.z < 0:
                self.z = tunnel_depth
                self.x = random.uniform(-tunnel_width / 2, tunnel_width / 2)
                self.y = random.uniform(-tunnel_height / 2, tunnel_height / 2)

        def draw(self, surface):
            if self.z <= 0:
                return
            # Perspective projection
            scale = 1 / (self.z + 0.1)  # Avoid division by zero
            # Apply ship's rotation to asteroid's (x,y)
            dx = self.x - ship['x']
            dy = self.y - ship['y']
            rot = ship['rotation']
            rot_x = dx * math.cos(rot) - dy * math.sin(rot)
            rot_y = dx * math.sin(rot) + dy * math.cos(rot)
            screen_x = screen_width / 2 + rot_x * screen_width * scale
            screen_y = screen_height / 2 - rot_y * screen_height * scale
            screen_radius = self.radius * screen_width * scale
            if 0 <= screen_x <= screen_width and 0 <= screen_y <= screen_height:
                pygame.draw.circle(surface, GREEN, (int(screen_x), int(screen_y)), int(screen_radius), 1)

        def is_hit(self, flare):
            dx = self.x - flare.x
            dy = self.y - flare.y
            dz = self.z - flare.z
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            return dist < self.radius

    class Flare:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
            self.speed = 0.2

        def update(self):
            self.z += self.speed

        def draw(self, surface):
            if self.z <= 0 or self.z > tunnel_depth:
                return
            # Perspective projection
            scale = 1 / (self.z + 0.1)
            dx = self.x - ship['x']
            dy = self.y - ship['y']
            rot = ship['rotation']
            rot_x = dx * math.cos(rot) - dy * math.sin(rot)
            rot_y = dx * math.sin(rot) + dy * math.cos(rot)
            screen_x = screen_width / 2 + rot_x * screen_width * scale
            screen_y = screen_height / 2 - rot_y * screen_height * scale
            flare_size = 5 * scale
            if 0 <= screen_x <= screen_width and 0 <= screen_y <= screen_height:
                pygame.draw.line(surface, GREEN, (screen_x, screen_y), (screen_x, screen_y - flare_size), 1)

    def generate_tunnel_segment(z):
        offset_x = math.sin(z * 0.5) * 0.5  # Smooth tunnel curve
        offset_y = math.cos(z * 0.5) * 0.5
        return {
            'z': z,
            'left': -tunnel_width / 2 + offset_x,
            'right': tunnel_width / 2 + offset_x,
            'top': -tunnel_height / 2 + offset_y,
            'bottom': tunnel_height / 2 + offset_y
        }

    # Initialize tunnel
    for i in range(tunnel_depth):
        tunnel_segments.append(generate_tunnel_segment(i))

    # Game loop
    clock = pygame.time.Clock()
    running = True
    last_asteroid_spawn = 0
    asteroid_spawn_interval = 2000  # milliseconds
    last_flare_time = 0
    flare_cooldown = 200  # milliseconds

    signal.signal(signal.SIGINT, handle_sigint)

    while running:
        current_time = pygame.time.get_ticks()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_time - last_flare_time > flare_cooldown:
                    flares.append(Flare(ship['x'], ship['y'], 0))
                    SND_FIRE.play()
                    last_flare_time = current_time
                elif event.key == pygame.K_w:
                    tunnel_speed += 0.03
                    SND_SPEEDUP.play()
                elif event.key == pygame.K_s:
                    tunnel_speed = max(0.01, tunnel_speed - 0.03)
                    SND_SLOWDOWN.play()
                elif event.key == pygame.K_a:
                    ship['x'] = max(-tunnel_width / 2, ship['x'] - ship['speed'])
                    SND_MOVE.play()
                elif event.key == pygame.K_d:
                    ship['x'] = min(tunnel_width / 2, ship['x'] + ship['speed'])
                    SND_MOVE.play()
                elif event.key == pygame.K_r:
                    ship['y'] = min(tunnel_height / 2, ship['y'] + ship['speed'])
                    SND_MOVE.play()
                elif event.key == pygame.K_f:
                    ship['y'] = max(-tunnel_height / 2, ship['y'] - ship['speed'])
                    SND_MOVE.play()
                elif event.key == pygame.K_q:
                    ship['rotation'] -= math.pi / 18  # 10 degrees
                    SND_ROTATE.play()
                elif event.key == pygame.K_e or event.key == pygame.K_RIGHT:
                    ship['rotation'] += math.pi / 18  # 10 degrees
                    SND_ROTATE.play()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Ship movement with arrow keys as alternatives
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship['x'] = max(-tunnel_width / 2, ship['x'] - ship['speed'])
        if keys[pygame.K_RIGHT]:
            ship['x'] = min(tunnel_width / 2, ship['x'] + ship['speed'])
        if keys[pygame.K_UP]:
            ship['y'] = min(tunnel_height / 2, ship['y'] + ship['speed'])
        if keys[pygame.K_DOWN]:
            ship['y'] = max(-tunnel_height / 2, ship['y'] - ship['speed'])

        # Spawn asteroids
        if current_time - last_asteroid_spawn > asteroid_spawn_interval:
            asteroids.append(Asteroid())
            last_asteroid_spawn = current_time

        # Update tunnel
        for segment in tunnel_segments:
            segment['z'] -= tunnel_speed
            if segment['z'] < 0:
                segment.update(generate_tunnel_segment(tunnel_depth))

        # Update asteroids
        for asteroid in asteroids:
            asteroid.update()

        # Update flares
        for flare in flares[:]:
            flare.update()
            if flare.z > tunnel_depth:
                flares.remove(flare)

        # Collision detection
        for asteroid in asteroids[:]:
            for flare in flares[:]:
                if asteroid.is_hit(flare):
                    asteroids.remove(asteroid)
                    flares.remove(flare)
                    SND_HIT.play()
                    break

        # Draw everything
        screen.fill(BLACK)

        # Draw tunnel (perspective projection)
        for segment in sorted(tunnel_segments, key=lambda s: s['z'], reverse=True):
            if segment['z'] <= 0:
                continue
            scale = 1 / (segment['z'] + 0.1)
            # Apply ship's rotation to tunnel walls
            for key in ['left', 'right']:
                dx = segment[key] - ship['x']
                dy = -tunnel_height / 2 - ship['y']
                rot = ship['rotation']
                segment[key + '_x'] = screen_width / 2 + (dx * math.cos(rot) - dy * math.sin(rot)) * screen_width * scale
                segment['top_y'] = screen_height / 2 - (dx * math.sin(rot) + dy * math.cos(rot)) * screen_height * scale
                dy = tunnel_height / 2 - ship['y']
                segment[key + '_bx'] = screen_width / 2 + (dx * math.cos(rot) - dy * math.sin(rot)) * screen_width * scale
                segment['bottom_y'] = screen_height / 2 - (dx * math.sin(rot) + dy * math.cos(rot)) * screen_height * scale

            next_idx = (tunnel_segments.index(segment) + 1) % len(tunnel_segments)
            next_segment = tunnel_segments[next_idx]
            next_scale = 1 / (next_segment['z'] + 0.1)
            for key in ['left', 'right']:
                dx = next_segment[key] - ship['x']
                dy = -tunnel_height / 2 - ship['y']
                rot = ship['rotation']
                next_segment[key + '_x'] = screen_width / 2 + (dx * math.cos(rot) - dy * math.sin(rot)) * screen_width * next_scale
                next_segment['top_y'] = screen_height / 2 - (dx * math.sin(rot) + dy * math.cos(rot)) * screen_height * next_scale
                dy = tunnel_height / 2 - ship['y']
                next_segment[key + '_bx'] = screen_width / 2 + (dx * math.cos(rot) - dy * math.sin(rot)) * screen_width * next_scale
                next_segment['bottom_y'] = screen_height / 2 - (dx * math.sin(rot) + dy * math.cos(rot)) * screen_height * next_scale

            # Draw tunnel walls
            pygame.draw.line(screen, GREEN, (segment['left_x'], segment['top_y']), (next_segment['left_x'], next_segment['top_y']), 1)
            pygame.draw.line(screen, GREEN, (segment['right_x'], segment['top_y']), (next_segment['right_x'], next_segment['top_y']), 1)
            pygame.draw.line(screen, GREEN, (segment['left_bx'], segment['bottom_y']), (next_segment['left_bx'], next_segment['bottom_y']), 1)
            pygame.draw.line(screen, GREEN, (segment['right_bx'], segment['bottom_y']), (next_segment['right_bx'], next_segment['bottom_y']), 1)

        # Draw asteroids
        for asteroid in asteroids:
            asteroid.draw(screen)

        # Draw flares
        for flare in flares:
            flare.draw(screen)

        # Draw crosshair for aiming
        pygame.draw.line(screen, GREEN, (screen_width / 2 - 10, screen_height / 2), (screen_width / 2 + 10, screen_height / 2), 1)
        pygame.draw.line(screen, GREEN, (screen_width / 2, screen_height / 2 - 10), (screen_width / 2, screen_height / 2 + 10), 1)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run Flask server in a separate thread
def start_server():
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == "__main__":
    # Handle Ctrl+C globally
    signal.signal(signal.SIGINT, handle_sigint)

    # Start Flask server in a thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

  
    # Run the Pygame game
    run_game()
