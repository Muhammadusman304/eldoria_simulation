import tkinter as tk
from tkinter import ttk, messagebox

from entities.entity import EntityType
from entities.hunter import HunterSkill
from entities.treasure import TreasureType
from simulation import EldoriaSimulation
from PIL import Image, ImageTk
import random
import time
from threading import Thread


class EldoriaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Eldoria Treasure Hunt Simulation")

        # Simulation variables
        self.simulation = None
        self.is_running = False
        self.speed = 500  # ms between updates
        self.cell_size = 30

        # Load images
        self.load_icons()

        # Create GUI components
        self.create_control_panel()
        self.create_grid_canvas()
        self.create_status_panel()

        # Start with default simulation
        self.create_simulation(20, 20)

    def load_icons(self):
        """Load and resize icons for grid display"""
        icon_size = (self.cell_size, self.cell_size)

        # Create simple colored icons if real images aren't available
        self.icons = {
            'empty': self.create_colored_icon('gray'),
            'hunter_N': self.create_colored_icon('blue'),
            'hunter_E': self.create_colored_icon('green'),
            'hunter_S': self.create_colored_icon('purple'),
            'knight': self.create_colored_icon('red'),
            'hideout': self.create_colored_icon('brown'),
            'treasure_B': self.create_colored_icon('#CD7F32'),  # bronze
            'treasure_S': self.create_colored_icon('#C0C0C0'),  # silver
            'treasure_G': self.create_colored_icon('#FFD700'),  # gold
        }

    def create_colored_icon(self, color):
        """Create a simple colored square icon"""
        image = Image.new('RGB', (self.cell_size, self.cell_size), color)
        return ImageTk.PhotoImage(image)

    def create_control_panel(self):
        """Create the control panel frame"""
        control_frame = ttk.LabelFrame(self.root, text="Simulation Controls", padding=10)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Grid size controls
        ttk.Label(control_frame, text="Grid Width:").grid(row=0, column=0, sticky="w")
        self.width_var = tk.IntVar(value=20)
        ttk.Spinbox(control_frame, from_=10, to=50, textvariable=self.width_var).grid(row=0, column=1)

        ttk.Label(control_frame, text="Grid Height:").grid(row=1, column=0, sticky="w")
        self.height_var = tk.IntVar(value=20)
        ttk.Spinbox(control_frame, from_=10, to=50, textvariable=self.height_var).grid(row=1, column=1)

        # Control buttons
        ttk.Button(control_frame, text="New Simulation", command=self.new_simulation).grid(row=2, column=0,
                                                                                           columnspan=2, pady=5)

        self.start_button = ttk.Button(control_frame, text="Start", command=self.toggle_simulation)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Speed control
        ttk.Label(control_frame, text="Speed:").grid(row=4, column=0, sticky="w")
        self.speed_var = tk.IntVar(value=500)
        ttk.Scale(control_frame, from_=50, to=1000, variable=self.speed_var,
                  orient=tk.HORIZONTAL, command=self.update_speed).grid(row=4, column=1)

        # Step control
        ttk.Button(control_frame, text="Step", command=self.step_simulation).grid(row=5, column=0, columnspan=2, pady=5)

    def create_grid_canvas(self):
        """Create the canvas for displaying the grid"""
        self.canvas_frame = ttk.LabelFrame(self.root, text="Eldoria Kingdom", padding=10)
        self.canvas_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.canvas = tk.Canvas(self.canvas_frame, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights to allow resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def create_status_panel(self):
        """Create the status panel frame"""
        status_frame = ttk.LabelFrame(self.root, text="Simulation Status", padding=10)
        status_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Statistics labels
        self.stats_vars = {
            'steps': tk.StringVar(),
            'hunters': tk.StringVar(),
            'active_hunters': tk.StringVar(),
            'knights': tk.StringVar(),
            'treasures': tk.StringVar(),
            'collected_treasures': tk.StringVar(),
            'hideouts': tk.StringVar()
        }

        for i, (label, var) in enumerate(self.stats_vars.items()):
            ttk.Label(status_frame, text=label.replace('_', ' ').title() + ":").grid(row=i, column=0, sticky="w")
            ttk.Label(status_frame, textvariable=var).grid(row=i, column=1, sticky="e")

        # Legend
        ttk.Label(status_frame, text="\nLegend:").grid(row=len(self.stats_vars), column=0, sticky="w", columnspan=2)

        legend_items = [
            ("Hunter (Navigation)", "hunter_N"),
            ("Hunter (Endurance)", "hunter_E"),
            ("Hunter (Stealth)", "hunter_S"),
            ("Knight", "knight"),
            ("Hideout", "hideout"),
            ("Bronze Treasure", "treasure_B"),
            ("Silver Treasure", "treasure_S"),
            ("Gold Treasure", "treasure_G")
        ]

        for i, (text, icon_key) in enumerate(legend_items, start=len(self.stats_vars) + 1):
            ttk.Label(status_frame, image=self.icons[icon_key], compound=tk.LEFT,
                      text=text).grid(row=i, column=0, sticky="w", columnspan=2)

    def create_simulation(self, width, height):
        """Create a new simulation with given dimensions"""
        if self.is_running:
            self.toggle_simulation()  # Stop current simulation

        self.simulation = EldoriaSimulation(width, height)
        self.draw_grid()
        self.update_stats()

    def new_simulation(self):
        """Create a new simulation based on current settings"""
        width = self.width_var.get()
        height = self.height_var.get()
        self.create_simulation(width, height)

    def toggle_simulation(self):
        """Start or stop the simulation"""
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Start")
        else:
            self.is_running = True
            self.start_button.config(text="Stop")
            Thread(target=self.run_simulation, daemon=True).start()

    def run_simulation(self):
        """Run the simulation in a separate thread"""
        while self.is_running and self.simulation.is_running():
            self.step_simulation()
            time.sleep(self.speed / 1000)

        if not self.simulation.is_running():
            self.is_running = False
            self.start_button.config(text="Start")
            messagebox.showinfo("Simulation Ended", "The simulation has completed!")

    def step_simulation(self):
        """Advance the simulation by one step"""
        if self.simulation:
            self.simulation.step()
            self.draw_grid()
            self.update_stats()

    def update_speed(self, *args):
        """Update simulation speed from slider"""
        self.speed = self.speed_var.get()

    def draw_grid(self):
        """Draw the current state of the grid"""
        if not self.simulation:
            return

        self.canvas.delete("all")

        # Calculate canvas size and cell dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        grid_width = self.simulation.grid.width
        grid_height = self.simulation.grid.height

        cell_width = canvas_width / grid_width
        cell_height = canvas_height / grid_height

        # Draw grid cells
        for x in range(grid_width):
            for y in range(grid_height):
                x1 = x * cell_width
                y1 = y * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                entity = self.simulation.grid.get_entity((x, y))
                icon_key = self.get_icon_key(entity)

                # Draw cell background
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray90", outline="gray80")

                # Draw entity icon if present
                if icon_key:
                    icon = self.icons[icon_key]
                    self.canvas.create_image(
                        x1 + cell_width / 2,
                        y1 + cell_height / 2,
                        image=icon
                    )

        # Draw grid lines
        for x in range(grid_width + 1):
            self.canvas.create_line(
                x * cell_width, 0,
                x * cell_width, canvas_height,
                fill="gray80"
            )
        for y in range(grid_height + 1):
            self.canvas.create_line(
                0, y * cell_height,
                canvas_width, y * cell_height,
                fill="gray80"
            )

    def get_icon_key(self, entity):
        """Determine which icon to use for an entity"""
        if not entity:
            return None

        if entity.type == EntityType.HUNTER:
            if entity.skill == HunterSkill.NAVIGATION:
                return 'hunter_N'
            elif entity.skill == HunterSkill.ENDURANCE:
                return 'hunter_E'
            else:
                return 'hunter_S'
        elif entity.type == EntityType.KNIGHT:
            return 'knight'
        elif entity.type == EntityType.HIDEOUT:
            return 'hideout'
        elif entity.type == EntityType.TREASURE:
            if entity.treasure_type == TreasureType.BRONZE:
                return 'treasure_B'
            elif entity.treasure_type == TreasureType.SILVER:
                return 'treasure_S'
            else:
                return 'treasure_G'
        return None

    def update_stats(self):
        """Update the statistics display"""
        if not self.simulation:
            return

        stats = self.simulation.get_stats()
        for key, var in self.stats_vars.items():
            var.set(str(stats[key]))


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    gui = EldoriaGUI(root)
    root.mainloop()