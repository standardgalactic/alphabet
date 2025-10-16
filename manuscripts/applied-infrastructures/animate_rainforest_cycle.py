"""
Animated illustration: Rainforest Generator (Atmospheric Moisture Cycle)
Shows evaporation, condensation, rainfall, and downdraft circulation.

Outputs:
    rainforest_cycle.gif
    rainforest_cycle.mp4

Dependencies:
    pip install matplotlib numpy pillow
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

plt.style.use("classic")

def animate_rainforest_cycle(n_frames=250, save_gif=True, save_mp4=True):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Ground line and canopy
    ax.plot([-3, 3], [1, 1], color="black", lw=2)
    canopy = plt.Circle((0, 1.5), 1.2, color="#3c6", alpha=0.3)
    ax.add_patch(canopy)
    ax.text(-2.9, 0.3, "Evaporation Zone", fontsize=9)
    ax.text(-2.9, 5.4, "Condensation Zone", fontsize=9)

    # Define parameters for particles
    n_drops = 30
    # positions of rising vapor (x,y) and falling rain
    vapor_x = np.random.uniform(-1, 1, n_drops)
    vapor_y = np.random.uniform(1.0, 3.0, n_drops)
    rain_x = np.random.uniform(-1, 1, n_drops)
    rain_y = np.random.uniform(3.5, 6.0, n_drops)

    vapor = ax.scatter(vapor_x, vapor_y, s=20, color="#99d", alpha=0.6)
    rain = ax.scatter(rain_x, rain_y, s=25, color="#55a", alpha=0.6)

    # Cloud layer
    cloud = plt.Circle((0, 4.5), 1.5, color="#ccc", alpha=0.4)
    ax.add_patch(cloud)

    def update(frame):
        # Rising vapor: move upward slowly, loop back when reaching cloud
        vapor_y[:] += 0.02
        vapor_y[vapor_y > 4.3] = np.random.uniform(1.0, 2.0, np.sum(vapor_y > 4.3))
        vapor_x[:] += 0.005 * np.sin(frame/10 + vapor_x)
        vapor.set_offsets(np.c_[vapor_x, vapor_y])

        # Falling rain: move downward, reset when hitting ground
        rain_y[:] -= 0.05
        rain_y[rain_y < 1.0] = np.random.uniform(4.5, 6.0, np.sum(rain_y < 1.0))
        rain_x[:] += 0.003 * np.sin(frame/15 + rain_x)
        rain.set_offsets(np.c_[rain_x, rain_y])

        return vapor, rain

    ani = FuncAnimation(fig, update, frames=n_frames, interval=50, blit=True)

    if save_gif:
        ani.save("rainforest_cycle.gif", writer=PillowWriter(fps=20))
        print("Saved rainforest_cycle.gif")
    if save_mp4:
        ani.save("rainforest_cycle.mp4", writer=FFMpegWriter(fps=20))
        print("Saved rainforest_cycle.mp4")

    plt.close()

if __name__ == "__main__":
    animate_rainforest_cycle()

