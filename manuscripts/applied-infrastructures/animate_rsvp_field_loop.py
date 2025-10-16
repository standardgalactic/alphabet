"""
RSVP Field-Driven Planetary Loop
Convection and rainfall intensities respond to a simulated entropy field S(x,t).
Outputs:
    rsvp_field_loop.gif
    rsvp_field_loop.mp4
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

plt.style.use("classic")

def simulate_entropy_field(nx=200, ny=100, n_steps=400, dt=0.02, D=0.2):
    """
    Generates a simple evolving entropy field S(x,t) by solving
        ∂S/∂t = D ∇²S  + forcing
    on a rectangular grid.
    """
    S = np.zeros((ny, nx))
    # initial heat spot (caldera)
    S[:, :] = 0.0
    S[ny//4:ny//2, nx//6:nx//3] = 1.0

    kernel = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    states = []
    for step in range(n_steps):
        lap = (
            np.roll(S,1,0)+np.roll(S,-1,0)+
            np.roll(S,1,1)+np.roll(S,-1,1)-4*S
        )
        S += D*lap*dt
        # slow periodic geothermal forcing
        S[ny//4:ny//2, nx//6:nx//3] += 0.01*np.sin(step*0.05)
        # slight cooling at top (radiation)
        S[-5:,:] *= 0.99
        # clip
        S = np.clip(S, 0, 1.5)
        if step % 5 == 0:
            states.append(S.copy())
    return states


def animate_rsvp_field_loop():
    states = simulate_entropy_field()
    n_frames = len(states)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-2, 6)
    ax.axis("off")

    # background heatmap (entropy field)
    extent = [-5, 5, -2, 6]
    im = ax.imshow(states[0], extent=extent, origin="lower",
                   cmap="inferno", alpha=0.5, aspect="auto")

    # base terrain lines
    ax.plot([-5,5],[0,0], color="black", lw=2)
    ax.plot([-1,1],[1,1], color="#2a2", lw=2)
    ax.text(-4.5,-1.7,"Caldera Reactor",fontsize=9)
    ax.text(2.5,5.4,"Condensation Zone",fontsize=9)
    ax.text(2.0,0.3,"Rainforest Basin",fontsize=9)

    # particle populations
    n_vapor, n_rain = 25, 25
    vapor_x = np.random.uniform(1.5,3.5,n_vapor)
    vapor_y = np.random.uniform(1.0,3.0,n_vapor)
    rain_x  = np.random.uniform(1.5,3.5,n_rain)
    rain_y  = np.random.uniform(3.5,6.0,n_rain)
    vapor = ax.scatter(vapor_x,vapor_y,s=20,color="#99d",alpha=0.6)
    rain  = ax.scatter(rain_x,rain_y,s=22,color="#55a",alpha=0.6)

    txt = ax.text(-4.7,5.3,"Entropy-Coupled Loop",fontsize=10,weight="bold")

    def update(i):
        S = states[i]
        im.set_data(S)

        # sample entropy near caldera to drive vapor intensity
        e_val = np.mean(S[25:45,25:35])
        up_speed = 0.015 + 0.05*e_val

        # rising vapor proportional to entropy
        vapor_y[:] += up_speed
        vapor_y[vapor_y>4.3] = np.random.uniform(1.0,2.0,np.sum(vapor_y>4.3))
        vapor.set_offsets(np.c_[vapor_x,vapor_y])
        vapor.set_alpha(0.4+0.4*e_val)

        # rainfall proportional to global entropy gradient
        grad = np.mean(np.abs(np.gradient(S)))
        rain_y[:] -= 0.02 + 0.1*grad
        rain_y[rain_y<1.0] = np.random.uniform(4.5,6.0,np.sum(rain_y<1.0))
        rain.set_offsets(np.c_[rain_x,rain_y])
        rain.set_alpha(0.3+0.5*grad)

        txt.set_text(f"Entropy-Coupled Loop — Step {i:03d}")
        return [im,vapor,rain,txt]

    ani = FuncAnimation(fig, update, frames=n_frames, interval=60, blit=True)

    ani.save("rsvp_field_loop.gif", writer=PillowWriter(fps=20))
    ani.save("rsvp_field_loop.mp4", writer=FFMpegWriter(fps=20))
    plt.close()
    print("Saved rsvp_field_loop.gif and rsvp_field_loop.mp4")

if __name__ == "__main__":
    animate_rsvp_field_loop()

