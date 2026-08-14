# Interactive Physics Balance Scale — using Tkinter

A GUI Python simulation featuring 2D physics fall animation, custom material density properties, interactive Drag & Drop mechanics, dynamic weight calculation, and responsive window scaling

---

## Simulation Mechanics & Features
* **20 Predefined Materials:** Real-world materials (Water, Gold, Titanium, Aerogel Air, Diamond, etc.) with fixed density calculations ($1\text{ m}^3$ scale volume).
* **Drag & Drop Engine:** Click and drag any block across the canvas with Z-index layering (raised active block depth).
* **Gravity Engine:** Automated falling logic to dual resting surfaces (scale platform vs. floor boundary).
* **Precision Weight Scale:** Real-time mass summation active only for cubes residing 100% within the platform span.
* **Responsive Layout:** Dynamic window resize handling with auto-centered scale platform positioning.

---

## How to Run

### Prerequisites
* Python 3.x installed (includes standard `tkinter`)

### To Run
1. Clone or download this repository
2. Run the application

### Repository Structure
1. main.py: Tkinter application, drag-and-drop controller, and physical scale engine.
2. specifications.md: Project physics requirements and functional specifications.
3. examples.txt: Complete application behavior walkthrough and test procedures.
