#!/usr/bin/python3

from flask import Flask, Response, render_template_string
import time
import random

app = Flask(__name__)

WIDTH, HEIGHT = 40, 20

def create_grid():
    return [[random.choice([0, 1]) for _ in range(WIDTH)] for __ in range(HEIGHT)]

def count_neighbors(grid, x, y):
    neighbors = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % WIDTH, (y + dy) % HEIGHT
            neighbors += grid[ny][nx]
    return neighbors

def step(grid):
    new_grid = [[0]*WIDTH for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            alive = grid[y][x]
            n = count_neighbors(grid, x, y)
            if alive and (n == 2 or n == 3):
                new_grid[y][x] = 1
            elif not alive and n == 3:
                new_grid[y][x] = 1
            else:
                new_grid[y][x] = 0
    return new_grid

def grid_to_text(grid):
    lines = []
    for row in grid:
        line = ''.join('█' if cell else ' ' for cell in row)
        lines.append(line)
    return '\n'.join(lines)

@app.route('/')
def index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Retro Game of Life 2D</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
  html, body {
    margin: 0; height: 100%;
    background: #000;
    color: #0f0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 18px;
    line-height: 1.1;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  #container {
    position: relative;
    padding: 20px 30px;
    background: #001100;
    box-shadow:
      0 0 10px #0f0,
      0 0 30px #0f0,
      inset 0 0 20px #0f0;
    border-radius: 6px;
    user-select: none;
    width: fit-content;
    max-width: 90vw;
    max-height: 90vh;
  }
  pre#life {
    margin: 0;
    white-space: pre; /* preserve newlines */
    font-family: 'Share Tech Mono', monospace;
    font-size: 18px;
    line-height: 1.1;
    filter: drop-shadow(0 0 2px #00ff00);
    letter-spacing: 0;
    user-select: none;
    position: relative;
  }
  /* Scanlines */
  body::before {
    content: "";
    pointer-events: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
      repeating-linear-gradient(
        0deg,
        rgba(0, 255, 0, 0.07) 0,
        rgba(0, 255, 0, 0.07) 1px,
        transparent 1px,
        transparent 3px
      );
    z-index: 10;
  }
  /* Slight glitch effect */
  @keyframes glitch {
    0% {
      clip: rect(0, 9999px, 0, 0);
      transform: translate(0);
    }
    20% {
      clip: rect(2px, 9999px, 8px, 0);
      transform: translate(-1px, 1px);
    }
    40% {
      clip: rect(4px, 9999px, 12px, 0);
      transform: translate(1px, -1px);
    }
    60% {
      clip: rect(3px, 9999px, 9px, 0);
      transform: translate(-1px, 0);
    }
    80% {
      clip: rect(5px, 9999px, 10px, 0);
      transform: translate(1px, 1px);
    }
    100% {
      clip: rect(0, 9999px, 0, 0);
      transform: translate(0);
    }
  }
  #life::before,
  #life::after {
    content: attr(data-text);
    position: absolute;
    left: 0; top: 0;
    width: 100%;
    color: #0f0;
    background: transparent;
    overflow: hidden;
  }
  #life::before {
    animation: glitch 2s infinite linear alternate-reverse;
    clip: rect(0, 9999px, 2px, 0);
    opacity: 0.6;
    left: 1px;
    text-shadow: -1px 0 #00ff00;
  }
  #life::after {
    animation: glitch 3s infinite linear alternate;
    clip: rect(3px, 9999px, 6px, 0);
    opacity: 0.4;
    left: -1px;
    text-shadow: 1px 0 #00ff00;
  }
</style>
</head>
<body>
  <div id="container">
    <h1>Conway's Game of Life</h1>
    <pre id="life" data-text=""></pre>
  </div>

<script>
  const evtSource = new EventSource("/stream");
  const pre = document.getElementById("life");
  evtSource.onmessage = function(event) {
    pre.textContent = event.data;
    pre.setAttribute('data-text', event.data);
  };
</script>
</body>
</html>
"""
    return render_template_string(html)

def event_stream():
    grid = create_grid()
    while True:
        text = grid_to_text(grid)
        yield f"data: {text}\n\n"
        grid = step(grid)
        time.sleep(0.15)  # 150ms per frame for smooth animation

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

