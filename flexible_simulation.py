import tkinter as tk
from tkinter import ttk, messagebox
from simulation import EldoriaSimulation
from threading import Thread
import time


def get_entity_symbol(entity):
    """Return a symbol for each entity type"""
    if entity.type.name == "HUNTER":
        return "H"
    elif entity.type.name == "KNIGHT":
        return "K"
    elif entity.type.name == "HIDEOUT":
        return "⛺"
    elif entity.type.name == "TREASURE":
        return {"BRONZE": "B", "SILVER": "S", "GOLD": "G"}[entity.treasure_type.name]
    return ""


class FlexibleEldoriaSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Eldoria Simulation Controller")
        self.root.geometry("800x600")

        # Simulation control variables
        self.simulation = None
        self.is_running = False
        self.speed = 300
        self.mode = "manual"  # or "auto"

        # Create GUI components
        self.create_mode_selector()
        self.create_control_panel()
        self.create_grid_canvas()
        self.create_status_panel()

        # Start with default simulation
        self.create_simulation(25, 25)

    def create_mode_selector(self):
        """Create the mode selection frame"""
        mode_frame = ttk.LabelFrame(self.root, text="Simulation Mode", padding=10)
        mode_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.mode_var = tk.StringVar(value="manual")

        ttk.Radiobutton(mode_frame, text="Manual Control",
                        variable=self.mode_var, value="manual",
                        command=self.change_mode).grid(row=0, column=0, padx=5)

        ttk.Radiobutton(mode_frame, text="Automatic Run",
                        variable=self.mode_var, value="auto",
                        command=self.change_mode).grid(row=0, column=1, padx=5)

    def change_mode(self):
        """Handle mode change"""
        new_mode = self.mode_var.get()
        if new_mode != self.mode:
            self.mode = new_mode
            if self.is_running:
                self.toggle_simulation()  # Stop current mode
            self.update_controls()

    def update_controls(self):
        """Update control availability based on mode"""
        if self.mode == "manual":
            self.step_button.config(state=tk.NORMAL)
            self.start_button.config(text="Start Auto")
        else:
            self.step_button.config(state=tk.DISABLED)
            self.start_button.config(text="Start")

    def create_control_panel(self):
        """Create the control panel frame"""
        control_frame = ttk.LabelFrame(self.root, text="Simulation Controls", padding=10)
        control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Grid size controls
        ttk.Label(control_frame, text="Grid Width:").grid(row=0, column=0, sticky="w")
        self.width_var = tk.IntVar(value=25)
        ttk.Spinbox(control_frame, from_=10, to=50, textvariable=self.width_var).grid(row=0, column=1)

        ttk.Label(control_frame, text="Grid Height:").grid(row=1, column=0, sticky="w")
        self.height_var = tk.IntVar(value=25)
        ttk.Spinbox(control_frame, from_=10, to=50, textvariable=self.height_var).grid(row=1, column=1)

        # Control buttons
        ttk.Button(control_frame, text="New Simulation", command=self.new_simulation).grid(row=2, column=0,
                                                                                           columnspan=2, pady=5)

        self.start_button = ttk.Button(control_frame, text="Start Auto", command=self.toggle_simulation)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.step_button = ttk.Button(control_frame, text="Step", command=self.step_simulation, state=tk.NORMAL)
        self.step_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Speed control
        ttk.Label(control_frame, text="Speed:").grid(row=5, column=0, sticky="w")
        self.speed_var = tk.IntVar(value=300)
        ttk.Scale(control_frame, from_=50, to=1000, variable=self.speed_var,
                  orient=tk.HORIZONTAL, command=self.update_speed).grid(row=5, column=1)

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
        status_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Statistics labels
        stats = ['steps', 'hunters', 'active_hunters', 'knights', 'treasures', 'collected_treasures', 'hideouts']
        self.stats_vars = {stat: tk.StringVar() for stat in stats}

        for i, stat in enumerate(stats):
            ttk.Label(status_frame, text=stat.replace('_', ' ').title() + ":").grid(row=i // 2, column=(i % 2) * 2,
                                                                                    sticky="w")
            ttk.Label(status_frame, textvariable=self.stats_vars[stat]).grid(row=i // 2, column=(i % 2) * 2 + 1,
                                                                             sticky="e")

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
        """Start or stop the simulation based on current mode"""
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Start Auto" if self.mode == "manual" else "Start")
        else:
            self.is_running = True
            self.start_button.config(text="Stop")

            if self.mode == "auto":
                Thread(target=self.run_auto_simulation, daemon=True).start()
            else:
                Thread(target=self.run_manual_simulation, daemon=True).start()

    def run_auto_simulation(self):
        """Run automatic simulation with proper visualization updates"""
        while self.is_running and self.simulation.is_running():
            self.simulation.step()
            self.root.after(0, self.update_display)  # Force GUI update
            time.sleep(self.speed / 1000)

        self.root.after(0, self.simulation_ended)

    def run_manual_simulation(self):
        """Manual mode just waits for step commands"""
        while self.is_running:
            time.sleep(0.1)
        self.root.after(0, self.simulation_ended)

    def simulation_ended(self):
        """Handle simulation completion"""
        if self.is_running:  # Only if not manually stopped
            self.is_running = False
            self.root.after(100, lambda: messagebox.showinfo(
                "Simulation Complete",
                f"Simulation ended after {self.simulation.steps} steps\n"
                f"Collected treasures: {self.simulation.get_stats()['collected_treasures']}"
            ))
            self.start_button.config(text="Start Auto" if self.mode == "manual" else "Start")

    def step_simulation(self):
        """Advance the simulation by one step (manual mode)"""
        if self.simulation and self.simulation.is_running():
            self.simulation.step()
            self.update_display()

    def update_speed(self, *args):
        """Update simulation speed from slider"""
        self.speed = self.speed_var.get()

    def update_display(self):
        """Force a full display update"""
        self.draw_grid()
        self.update_stats()
        self.canvas.update_idletasks()

    def draw_grid(self):
        """Properly draw the current state of the grid with visible entities"""
        self.canvas.delete("all")
        if not self.simulation:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        cell_width = canvas_width / self.simulation.grid.width
        cell_height = canvas_height / self.simulation.grid.height

        # Draw all entities
        for x in range(self.simulation.grid.width):
            for y in range(self.simulation.grid.height):
                x1 = x * cell_width
                y1 = y * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                entity = self.simulation.grid.get_entity((x, y))
                color = self.get_entity_color(entity)

                # Draw cell background
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color if color else "white",
                    outline="gray80",
                    width=1
                )

                # Add text label for entity type
                if entity:
                    text = get_entity_symbol(entity)
                    self.canvas.create_text(
                        x1 + cell_width / 2,
                        y1 + cell_height / 2,
                        text=text,
                        fill="black" if color else "gray"
                    )

    def get_entity_color(self, entity):
        """Get color for an entity"""
        if not entity:
            return None

        colors = {
            "HUNTER": {
                "NAVIGATION": "blue",
                "ENDURANCE": "green",
                "STEALTH": "purple"
            },
            "KNIGHT": "red",
            "HIDEOUT": "brown",
            "TREASURE": {
                "BRONZE": "#CD7F32",
                "SILVER": "#C0C0C0",
                "GOLD": "#FFD700"
            }
        }

        if entity.type.name == "HUNTER":
            return colors["HUNTER"][entity.skill.name]
        elif entity.type.name == "TREASURE":
            return colors["TREASURE"][entity.treasure_type.name]
        else:
            return colors.get(entity.type.name)

    def update_stats(self):
        """Update the statistics display"""
        if self.simulation:
            stats = self.simulation.get_stats()
            for key, var in self.stats_vars.items():
                var.set(str(stats[key]))


if __name__ == "__main__":
    root = tk.Tk()
    app = FlexibleEldoriaSimulation(root)
    root.mainloop()