Main Goal: Implement interactive Drag & Drop and simulated physical balance scales

Application Features:
1. Object Generation:
   - User chooses from 20 predefined materials.
   - User inputs the desired number of cubes to generate.
2. Interactive Control (Drag & Drop):
   - Any cube can be picked up with the left mouse button and moved anywhere within the window, preserving initial mouse click offsets.
   - Upon mouse release, the cube exits manual drag mode and falls back under physics simulation control.
3. Fall Physics:
   - Released cubes descend under gravity.
   - Cubes land on one of two support surfaces: the scale platform or the canvas floor.

Implementation Details:
- Cubes do not interact with each other (no collisions, stacking, or physical blocking).
- Fall animation completes when reaching a resting surface.
- Mass Display:
  - Total mass reflects only cubes positioned fully inside the horizontal boundaries of the scale and residing precisely on its top surface.
  - Mass is displayed in kilograms and updates dynamically in real time. Volume and mass of each cube are fixed (Volume = 1 m^3, Mass = Density in kg/m^3).
  - Fixed cube dimension (100x100 pixels).
  - Shape geometry: Cubes / Rectangles only.
  - Maximum single creation batch limit: 10 cubes.

- "Reset" button provided to clear all objects and reset platform weight to zero.
- Dynamic interface adaptation (scale platform remains centered at bottom on window resize).
