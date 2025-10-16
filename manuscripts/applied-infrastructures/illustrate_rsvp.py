"""
Procedural illustrations for RSVP and Applied RSVP volumes.
Generates schematic line art for:
1. Tetraorthodrome (air/energy exchange geometry)
2. Intervolsorial Pediment (layered water terraces)
3. Caldera Reactor (gravitational battery basin)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
plt.style.use("classic")

def savefig(name):
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(name, dpi=300, bbox_inches="tight", pad_inches=0.05)
    plt.close()
    print(f"Saved {name}")

# ---------------------------------------------------------------------
def tetraorthodrome():
    """Four-axis circulation geometry"""
    fig, ax = plt.subplots(figsize=(6,6))
    # Draw central hub
    hub = Circle((0,0), 0.2, fill=False, lw=2)
    ax.add_patch(hub)
    # Four arms
    for angle in [0, 90, 180, 270]:
        rad = np.deg2rad(angle)
        x = [0, np.cos(rad)]
        y = [0, np.sin(rad)]
        ax.plot(x, y, lw=3)
        ax.arrow(np.cos(rad)*0.7, np.sin(rad)*0.7,
                 0.15*np.cos(rad), 0.15*np.sin(rad),
                 width=0.02, head_length=0.1, color="black")
    ax.set_xlim(-1.2,1.2)
    ax.set_ylim(-1.2,1.2)
    ax.set_aspect("equal")
    savefig("illustration_tetraorthodrome.png")

# ---------------------------------------------------------------------
def intervolsorial_pediment():
    """Layered terraces showing salinity gradient"""
    fig, ax = plt.subplots(figsize=(8,4))
    patches=[]
    n_layers=5
    for i in range(n_layers):
        x0, y0 = 0, i*0.8
        w, h = 8 - i*0.8, 0.6
        terrace = Polygon([[x0,y0],[x0+w,y0+0.2],[x0+w,y0+h],[x0,y0+h-0.2]],
                          closed=True)
        patches.append(terrace)
    pc = PatchCollection(patches, cmap="copper", alpha=0.4, edgecolor="brown")
    pc.set_array(np.linspace(0.2,1.0,len(patches)))
    ax.add_collection(pc)
    ax.text(0.3, 3.9, "Surface Mangroves", fontsize=10, color="brown")
    ax.text(2.5, 2.2, "Kelp Zone", fontsize=10, color="brown")
    ax.text(5.0, 0.8, "Detrital Basin", fontsize=10, color="brown")
    ax.set_xlim(0,8)
    ax.set_ylim(0,5)
    ax.set_aspect("equal")
    savefig("illustration_intervolsorial_pediment.png")

# ---------------------------------------------------------------------
def caldera_reactor():
    """Cross-section of gravitational battery basin"""
    fig, ax = plt.subplots(figsize=(7,4))
    # crater walls
    theta = np.linspace(0, np.pi, 200)
    r_outer = 3 + 0.3*np.sin(3*theta)
    x_outer, y_outer = r_outer*np.cos(theta), r_outer*np.sin(theta)
    ax.plot(x_outer, y_outer, color="black", lw=2)
    # convection loops
    for x0 in [-1.5, 0, 1.5]:
        circ = plt.Circle((x0, -0.5), 0.8, fill=False, lw=1.5)
        ax.add_patch(circ)
        ax.arrow(x0, -1.3, 0, 0.5, head_width=0.1, color="black")
        ax.arrow(x0, 0.3, 0, -0.5, head_width=0.1, color="black")
    ax.text(-2.5,0.2,"Condensation",fontsize=9)
    ax.text(-0.5,-2.2,"Convection Cells",fontsize=9)
    ax.text(1.0,0.3,"Evaporation",fontsize=9)
    ax.set_xlim(-3.5,3.5)
    ax.set_ylim(-2.5,2.5)
    ax.set_aspect("equal")
    savefig("illustration_caldera_reactor.png")

# ---------------------------------------------------------------------
if __name__ == "__main__":
    tetraorthodrome()
    intervolsorial_pediment()
    caldera_reactor()

