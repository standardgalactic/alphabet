DOS THEORY VISUALIZER SUITE
===========================

This package contains small real-mode DOS .COM visualizers intended for DOSBox.
Each program switches to VGA mode 13h, draws a procedural animated field, and
exits back to text mode when any key is pressed.

Programs
--------
RSVP.COM     Scalar/vector/plenum style turbulent field.
REACH.COM    Expanding reachability wavefront geometry.
ADMISS.COM   Contour-like admissibility bands and fragile regions.
DISTINCT.COM Distinguishability partitions and cluster-like compression.
SPHERE.COM   Collapse rings and nested event shells.
MEM8.COM     Memory interference and trace-like persistence textures.
TARTAN.COM   Recursive tartan/plaid transformation field.
REPAIR.COM   Crack, repair, and continuation-field visualization.

Usage in DOSBox
---------------
mount c path_to_this_folder
c:
MENU
RSVP

Press any key to leave a visualizer.

Build notes
-----------
The .COM files are tiny 16-bit real-mode programs built from the included GNU
assembler source files. They do not require Windows, SDL, or external assets at
runtime. They are intentionally simple VGA instruments rather than modern GPU
visualizers.
