import time
from simulation import EldoriaSimulation
from gui.eldoria_gui import EldoriaGUI  # Reusing the GUI for visualization
import tkinter as tk
from threading import Thread


class AutomatedEldoriaSimulation:
    def __init__(self, width=30, height=30):
        self.root = tk.Tk()
        self.root.title("Eldoria Automated Simulation")
        self.root.geometry("1000x700")

        # Initialize simulation and GUI
        self.simulation = EldoriaSimulation(width, height)
        self.gui = EldoriaGUI(self.root)
        self.gui.simulation = self.simulation  # Connect to existing simulation

        # Configure for automatic running
        self.gui.is_running = True
        self.gui.start_button.config(text="Running...", state=tk.DISABLED)
        self.gui.speed_var.set(100)  # Faster than default

        # Start the simulation thread
        self.simulation_thread = Thread(target=self.run_simulation, daemon=True)
        self.simulation_thread.start()

        # Start the GUI update loop
        self.update_gui()

        self.root.mainloop()

    def run_simulation(self):
        """Run simulation to completion"""
        while self.gui.is_running and self.simulation.is_running():
            self.simulation.step()
            time.sleep(self.gui.speed / 1000)

        # Simulation ended
        self.gui.is_running = False
        self.root.after(100, self.show_completion_message)

    def update_gui(self):
        """Periodically update the GUI"""
        if self.gui.is_running:
            self.gui.draw_grid()
            self.gui.update_stats()
            self.root.after(200, self.update_gui)  # Update every 200ms

    def show_completion_message(self):
        """Show completion message when simulation ends"""
        stats = self.simulation.get_stats()
        message = (
            f"Simulation completed in {stats['steps']} steps!\n\n"
            f"Treasures collected: {stats['collected_treasures']}\n"
            f"Remaining treasures: {stats['treasures']}\n"
            f"Active hunters: {stats['active_hunters']}/{stats['hunters']}"
        )
        tk.messagebox.showinfo("Simulation Complete", message)
        self.root.destroy()


if __name__ == "__main__":
    AutomatedEldoriaSimulation(width=30, height=30)