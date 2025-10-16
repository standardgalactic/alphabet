"""
Planetary Thermodynamic Loop Animation
Combines:
 - Caldera Reactor (left): geothermal convection
 - Rainforest Generator (right): evaporation–condensation–rainfall
Outputs:
   planetary_loop.gif
   planetary_loop.mp4
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

plt.style.use("classic")

def animate_planetary_loop(n_frames=300, save_gif=True, save_mp4=True):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-2, 6)
    ax.axis("off")

    # --- Land, water, and canopy base lines ---
    ax.plot([-5, 5], [0, 0], color="black", lw=2)
    ax.plot([-1, 1], [1, 1], color="#2a2", lw=2)  # canopy line (forest)
    ax.text(-4.5, -1.7, "Caldera Reactor", fontsize=9)
    ax.text(2.5, 5.4, "Condensation Zone", fontsize=9)
    ax.text(1.8, 0.3, "Rainforest Basin", fontsize=9)

    # --- Caldera crater (left) ---
    theta = np.linspace(0, np.pi, 200)
    r_outer = 2 + 0.3 * np.sin(3 * theta)
    x_outer, y_outer = -3 + r_outer * np.cos(theta), -0.5 + r_outer * np.sin(theta)
    ax.plot(x_outer, y_outer, color="black", lw=1.8)

    # --- Vapor cloud over rainforest ---
    cloud = plt.Circle((2.5, 4.5), 1.5, color="#ccc", alpha=0.4)
    ax.add_patch(cloud)

    # --- Particle fields ---
    n_caldera = 40
    n_vapor = 25
    n_rain = 25

    # Caldera convection particles (warm loops)
    caldera_x0 = -3
    radii = [0.6, 1.1]
    caldera_particles = []
    for r in radii:
        theta0 = np.linspace(0, 2*np.pi, n_caldera, endpoint=False)
        x = caldera_x0 + r * np.cos(theta0)
        y = -0.5 + 0.5 * np.sin(theta0)
        sc = ax.scatter(x, y, s=18, color="#c66", alpha=0.7)
        caldera_particles.append((r, sc, np.random.rand()*2*np.pi))

    # Vapor rise over forest
    vapor_x = np.random.uniform(1.5, 3.5, n_vapor)
    vapor_y = np.random.uniform(1.0, 3.0, n_vapor)
    vapor = ax.scatter(vapor_x, vapor_y, s=20, color="#99d", alpha=0.6)

    # Rainfall
    rain_x = np.random.uniform(1.5, 3.5, n_rain)
    rain_y = np.random.uniform(3.5, 6.0, n_rain)
    rain = ax.scatter(rain_x, rain_y, s=22, color="#55a", alpha=0.6)

    # --- Annotation ---
    txt = ax.text(-4.7, 5.3, "Thermodynamic Loop", fontsize=10, weight="bold")

    # --- Frame update function ---
    def update(frame):
        # Caldera convection rotation
        for r, sc, phase in caldera_particles:
            theta = np.linspace(0, 2*np.pi, n_caldera, endpoint=False)
            theta = (theta + 0.05*frame + phase) % (2*np.pi)
            x = caldera_x0 + r * np.cos(theta)
            y = -0.5 + 0.5 * np.sin(theta)
            sc.set_offsets(np.c_[x, y])

        # Vapor rise
        vapor_y[:] += 0.02
        vapor_y[vapor_y > 4.3] = np.random.uniform(1.0, 2.0, np.sum(vapor_y > 4.3))
        vapor_x[:] += 0.005 * np.sin(frame/10 + vapor_x)
        vapor.set_offsets(np.c_[vapor_x, vapor_y])

        # Rainfall descent
        rain_y[:] -= 0.05
        rain_y[rain_y < 1.0] = np.random.uniform(4.5, 6.0, np.sum(rain_y < 1.0))
        rain_x[:] += 0.004 * np.sin(frame/15 + rain_x)
        rain.set_offsets(np.c_[rain_x, rain_y])

        txt.set_text(f"Thermodynamic Loop — Cycle {frame%100:02d}")
        return [sc for _, sc, _ in caldera_particles] + [vapor, rain, txt]

    ani = FuncAnimation(fig, update, frames=n_frames, interval=50, blit=True)

    if save_gif:
        ani.save("planetary_loop.gif", writer=PillowWriter(fps=20))
        print("Saved planetary_loop.gif")
    if save_mp4:
        ani.save("planetary_loop.mp4", writer=FFMpegWriter(fps=20))
        print("Saved planetary_loop.mp4")

    plt.close()

if __name__ == "__main__":
    animate_planetary_loop()

