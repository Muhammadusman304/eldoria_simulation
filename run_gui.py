import tkinter as tk
from gui.eldoria_gui import EldoriaGUI


def main():
    # Create the main window
    root = tk.Tk()
    root.title("Eldoria Treasure Hunt Simulation")

    # Set initial window size (adapts to content)
    root.geometry("1000x700")

    # Initialize and run the GUI
    app = EldoriaGUI(root)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()