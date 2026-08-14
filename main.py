import tkinter as tk
from tkinter import ttk, messagebox

# Materials dictionary: each element contains density (in kg/m^3) and visual color
# Density is used as the mass of one cube given a fixed volume (1 m^3)
materials = {
    "Water": {"density": 1000, "color": "#B0E0E6"},
    "Sand": {"density": 1600, "color": "#C2B280"},
    "Feathers": {"density": 25, "color": "#FFF5EE"},
    "Stone": {"density": 2500, "color": "gray"},
    "Diamond": {"density": 3500, "color": "#8EEBEC"},
    "Emerald": {"density": 2700, "color": "#50C878"},
    "Iron": {"density": 7870, "color": "#71797E"},
    "Wood": {"density": 700, "color": "#966F33"},
    "Ice": {"density": 917, "color": "#EBF4FA"},
    "Air": {"density": 1.2, "color": "whitesmoke"},
    "Cotton": {"density": 1500, "color": "linen"},
    "Salt Water": {"density": 1025, "color": "#008080"},
    "Marble": {"density": 2700, "color": "#E5D0CA"},
    "Plastic": {"density": 1400, "color": "yellow"},
    "Oil": {"density": 920, "color": "olive"},
    "Paper": {"density": 900, "color": "#F8F8FF"},
    "Concrete": {"density": 2400, "color": "dimgray"},
    "Titanium": {"density": 4500, "color": "silver"},
    "Coca-Cola": {"density": 1040, "color": "#4C2F27"},
    "White Gold": {"density": 15000, "color": "#c9c0bb"},
}

CUBE_SIZE = 100          # Cube side length in pixels
SCALE_WIDTH = 600        # Scale platform width in pixels
SCALE_HEIGHT = 50        # Scale platform height
GRAVITY_STEP = 6         # Maximum vertical displacement per animation tick
UPDATE_DELAY = 20        # Interval between animation frames in milliseconds

class ScalerGame:
    def __init__(self, root): # Create main window with title
        self.root = root
        self.root.title("Scales")
        self.root.geometry("1000x700")

        self.cubes = []  # Stores info for each cube (coordinates, mass, etc.)
        self.total_mass = 0  # Total mass of cubes sitting on the scale
        self.platform_id = None  # Platform element ID
        self.weight_text_id = None  # Mass display text ID
        self.dragged_cube = None  # Currently dragged cube (None if unselected)

        # Create control panel on the left
        control_frame = tk.Frame(root, width=200)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Create interactive canvas on the right for visuals
        self.canvas = tk.Canvas(root, bg="#fcebed")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Controls: material selection and quantity
        tk.Label(control_frame, text="Material:").pack(pady=(10, 0))
        self.material_var = tk.StringVar(value=list(materials.keys())[0])
        ttk.Combobox( # Materials selected from predefined dictionary
            control_frame, textvariable=self.material_var,
            values=list(materials.keys()), state="readonly"
        ).pack(pady=5)

        tk.Label(control_frame, text="Quantity:").pack()
        self.count_var = tk.StringVar(value="1")
        tk.Entry(control_frame, textvariable=self.count_var, width=10).pack()

        # Action buttons
        tk.Button(control_frame, text="Create cubes", command=self.create_cubes).pack(pady=10)
        tk.Button(control_frame, text="Reset", command=self.reset).pack()

        # Mouse event bindings for drag and drop
        self.canvas.bind("<Button-1>", self.on_click)  # Click
        self.canvas.bind("<B1-Motion>", self.on_drag)  # Drag
        self.canvas.bind("<ButtonRelease-1>", self.on_release)  # Release
        self.canvas.bind("<Configure>", self.on_resize)  # Window resize

        self.root.after(100, self.init_platform_and_weight) # Platform initialization and animation loop start
        self.animate_fall()

    def on_resize(self, event=None): # Handles canvas resize events
        self.init_platform_and_weight()

    def init_platform_and_weight(self): # Creates or updates visual scale platform and text
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 1 or h <= 1: # Ensure dimensions are valid
            return

        # Center scale platform at bottom of canvas with fixed width
        self.scale_x1 = (w - SCALE_WIDTH) // 2
        self.scale_x2 = self.scale_x1 + SCALE_WIDTH
        self.scale_y1 = h - SCALE_HEIGHT

        if self.platform_id: # Remove previous elements if existing
            self.canvas.delete(self.platform_id)
        if self.weight_text_id:
            self.canvas.delete(self.weight_text_id)

        self.platform_id = self.canvas.create_rectangle( # Draw platform
            self.scale_x1, self.scale_y1, self.scale_x2, h,
            fill="pink", outline="darkred", width=2
        )
        self.weight_text_id = self.canvas.create_text( # Mass label in center of platform
            w // 2, self.scale_y1 + SCALE_HEIGHT // 2,
            text="0 kg", font=("Arial", 16, "bold"), fill="white"
        )

    def create_cubes(self): # Generates specified number of cubes of selected material
        try:
            n = int(self.count_var.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid quantity of cubes!")
            return

        material = self.material_var.get()
        if material not in materials:
            messagebox.showerror("Error", "Unknown material!")
            return

        mat = materials[material]
        w = max(1, self.canvas.winfo_width())
        start_y = 50 # First row vertical offset

        for i in range(n):
            # Positioning in grid (up to 5 cubes per row across 2 rows)
            x = 80 + (i % 5) * (CUBE_SIZE + 20)
            y = start_y + (i // 5) * (CUBE_SIZE + 20)
            if x + CUBE_SIZE > w - 30 or y > 250: # Stop spawning if boundaries exceeded
                break

            rect = self.canvas.create_rectangle( # Create cube shape on canvas
                x, y, x + CUBE_SIZE, y + CUBE_SIZE,
                fill=mat["color"], outline="darkgray", width=2
            )
            self.cubes.append({ # Store cube state
                "id": rect, "material": material, "mass": mat["density"], "x": x, "y": y
            })

    def on_click(self, event): # Handles mouse button press
        # Detects if cursor is over a cube; if so, selects active cube and raises it to top
        # Reverse search ensures top-most overlapping cube takes priority
        for cube in reversed(self.cubes):
            x1, y1, x2, y2 = self.canvas.coords(cube["id"])
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.dragged_cube = cube
                self.offset_x = event.x - x1
                self.offset_y = event.y - y1
                self.canvas.tag_raise(cube["id"]) # Bring clicked cube to front
                break

    def on_drag(self, event): # Handles mouse movement while pressed
        if not self.dragged_cube:
            return
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height() # Constrain within canvas bounds
        new_x = max(0, min(event.x - self.offset_x, w - CUBE_SIZE))
        new_y = max(0, min(event.y - self.offset_y, h - CUBE_SIZE))

        dx, dy = new_x - self.dragged_cube["x"], new_y - self.dragged_cube["y"] # Calculate offset and move
        self.canvas.move(self.dragged_cube["id"], dx, dy)
        self.dragged_cube["x"], self.dragged_cube["y"] = new_x, new_y

    def on_release(self, event): # Handles mouse release
        self.dragged_cube = None # Clear active cube drag reference

    def animate_fall(self): # Simulates gravity fall mechanics
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            self.root.after(UPDATE_DELAY, self.animate_fall)
            return

        floor_y = h - CUBE_SIZE # Floor level off the scale
        scale_support_y = self.scale_y1 - CUBE_SIZE  # Surface level on scale

        for cube in self.cubes:
            if cube is self.dragged_cube:
                continue # Skip currently dragged cube

            # Check if cube is positioned above scale platform horizontal range
            on_scale_area = (cube["x"] + CUBE_SIZE > self.scale_x1 and
                             cube["x"] < self.scale_x2)

            if on_scale_area: # Determine surface target
                target_y = scale_support_y
            else:
                target_y = floor_y

            if cube["y"] < target_y:
                step = min(GRAVITY_STEP, target_y - cube["y"]) # Smooth fall toward target surface
                self.canvas.move(cube["id"], 0, step)
                cube["y"] += step
            elif abs(cube["y"] - target_y) > 0.1: # Precise snapping to target level
                dy = target_y - cube["y"]
                self.canvas.move(cube["id"], 0, dy)
                cube["y"] = target_y

        self.update_total_weight() # Update weight counter text
        self.root.after(UPDATE_DELAY, self.animate_fall) # Schedule next frame update

    def update_total_weight(self): # Sums total mass of cubes located fully on scale
        total = 0
        scale_support_y = self.scale_y1 - CUBE_SIZE
        for cube in self.cubes:
            # Cube must be entirely inside horizontal scale bounds
            on_scale_x = (cube["x"] >= self.scale_x1 and
                          cube["x"] + CUBE_SIZE <= self.scale_x2)
            on_scale_y = abs(cube["y"] - scale_support_y) < 2
            if on_scale_x and on_scale_y: # Add mass if fully resting on scale
                total += cube["mass"]
        self.total_mass = total
        if self.weight_text_id:
            self.canvas.itemconfig(self.weight_text_id, text=f"{self.total_mass:,.1f} kg") # Display mass on scale platform

    def reset(self): # Full board reset function
        for cube in self.cubes:
            self.canvas.delete(cube["id"])
        self.cubes.clear()
        self.total_mass = 0
        if self.weight_text_id:
            self.canvas.itemconfig(self.weight_text_id, text="0 kg")


def main(): # Entry point launching application loop
    root = tk.Tk()
    ScalerGame(root)
    root.mainloop()

main()
