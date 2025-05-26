#!/usr/bin/python3

from flask import Flask, Response, render_template_string
import time
import random

app = Flask(__name__)

WIDTH = 40
HEIGHT = 20

def create_grid():
    return [[random.choice([0,1]) for _ in range(WIDTH)] for _ in range(HEIGHT)]

def count_neighbors(grid, x, y):
    total = 0
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH:
                total += grid[nx][ny]
    return total

def update(grid):
    new_grid = [[0]*WIDTH for _ in range(HEIGHT)]
    for i in range(HEIGHT):
        for j in range(WIDTH):
            neighbors = count_neighbors(grid, i, j)
            if grid[i][j] == 1 and neighbors in [2,3]:
                new_grid[i][j] = 1
            elif grid[i][j] == 0 and neighbors == 3:
                new_grid[i][j] = 1
    return new_grid

def grid_to_text(grid):
    return "\n".join("".join("█" if cell else " " for cell in row) for row in grid)

@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Retro Game of Life</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
  html, body {
    margin: 0; height: 100%;
    background: #000;
    color: #0f0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 18px;
    line-height: 1.2;
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
  }
  pre {
    margin: 0;
    white-space: pre;
    filter:
      drop-shadow(0 0 2px #00ff00);
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
  /* Two layered pre elements for glitch */
  #life {
    position: relative;
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
    """)

@app.route("/stream")
def stream():
    def event_stream():
        grid = create_grid()
        while True:
            text = grid_to_text(grid)
            yield f"data: {text}\n\n"
            grid = update(grid)
            time.sleep(0.3)
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

