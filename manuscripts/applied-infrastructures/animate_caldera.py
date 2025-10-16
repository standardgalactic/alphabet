"""
Animated convection cycle for the Caldera Reactor.
Creates 'caldera_convection.gif' and 'caldera_convection.mp4'.

Requires: matplotlib, numpy, pillow, ffmpeg (for mp4)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

plt.style.use("classic")

def animate_caldera(n_frames=200, save_gif=True, save_mp4=True):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-2.0, 2.5)
    ax.axis("off")

    # Draw the crater walls
    theta = np.linspace(0, np.pi, 200)
    r_outer = 3 + 0.25*np.sin(3*theta)
    x_outer, y_outer = r_outer*np.cos(theta), r_outer*np.sin(theta)
    ax.plot(x_outer, y_outer, color="black", lw=2)

    # Define convection loop parameters
    n_particles = 40
    radii = np.linspace(0.6, 1.4, 3)
    colors = ["#b66", "#c77", "#d88"]  # warm tone palette
    particles = []
    for j, r in enumerate(radii):
        theta0 = np.linspace(0, 2*np.pi, n_particles, endpoint=False)
        x = r * np.cos(theta0)
        y = -0.5 + 0.5 * np.sin(theta0)
        sc = ax.scatter(x, y, s=20, color=colors[j], alpha=0.7)
        particles.append((r, sc, np.random.rand()*np.pi*2))

    txt = ax.text(-2.5, 1.9, "Updraft / Evaporation", fontsize=9)
    ax.text(-2.5, -1.6, "Downdraft / Condensation", fontsize=9)

    def update(frame):
        for r, sc, phase in particles:
            theta = np.linspace(0, 2*np.pi, n_particles, endpoint=False)
            # rotate points along the convection loop
            theta = (theta + 0.03*frame + phase) % (2*np.pi)
            x = r * np.cos(theta)
            y = -0.5 + 0.5 * np.sin(theta)
            sc.set_offsets(np.c_[x, y])
        txt.set_text(f"Cycle {frame%100:02d}")
        return [sc for _, sc, _ in particles] + [txt]

    ani = FuncAnimation(fig, update, frames=n_frames, interval=50, blit=True)

    if save_gif:
        ani.save("caldera_convection.gif", writer=PillowWriter(fps=20))
        print("Saved caldera_convection.gif")
    if save_mp4:
        ani.save("caldera_convection.mp4", writer=FFMpegWriter(fps=20))
        print("Saved caldera_convection.mp4")

    plt.close()

if __name__ == "__main__":
    animate_caldera()

