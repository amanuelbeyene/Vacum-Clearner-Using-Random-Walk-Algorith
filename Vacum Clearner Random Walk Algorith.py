import tkinter as tk
import random

class VacuumCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner Simulation")

        # Grid dimensions
        self.grid_size = 4
        self.cell_size = 100  # Will scale dynamically later

        # Create canvas
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.resize_canvas)

        # Initialize grid, rooms, vacuum, and dust particles
        self.room_types = self.create_room_types()
        self.dust_positions = set()
        self.vacuum_position = (0, 0)
        self.draw_rooms()
        self.place_dust()
        self.draw_vacuum()

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_cleaning, bg="green", fg="white", width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_cleaning, bg="red", fg="white", width=10)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Movement controls
        self.is_running = False
        self.root.bind("<Up>", lambda e: self.move_vacuum("up"))
        self.root.bind("<Down>", lambda e: self.move_vacuum("down"))
        self.root.bind("<Left>", lambda e: self.move_vacuum("left"))
        self.root.bind("<Right>", lambda e: self.move_vacuum("right"))

    def create_room_types(self):
        """Defines room types for the grid."""
        room_layout = [
            ["Bedroom", "Kitchen", "Living Room", "Bathroom"],
            ["Bedroom", "Kitchen", "Living Room", "Bathroom"],
            ["Office", "Dining Room", "Garage", "Hallway"],
            ["Office", "Dining Room", "Garage", "Hallway"]
        ]
        return room_layout

    def draw_rooms(self):
        """Draws the rooms on the canvas based on the room layout."""
        self.canvas.delete("room")
        colors = {
            "Bedroom": "#f0e68c",
            "Kitchen": "#add8e6",
            "Living Room": "#ffb6c1",
            "Dining Room": "#90ee90",
            "Bathroom": "#d3d3d3",
            "Garage": "#a9a9a9",
            "Hallway": "#ffffff",
            "Office": "#dda0dd"
        }

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                room_type = self.room_types[i][j]
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=colors.get(room_type, "white"), tags="room")
                self.canvas.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2,
                    text=room_type[:3], fill="black", font=("Arial", 10), tags="room"
                )

    def place_dust(self):
        """Randomly places dust particles within the grid."""
        self.dust_positions.clear()
        for _ in range(8):  # Number of dust particles
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            self.dust_positions.add((x, y))
            self.draw_dust(x, y)

    def draw_dust(self, x, y):
        """Draws a dust particle at the given position."""
        x1, y1 = x * self.cell_size + 15, y * self.cell_size + 15
        x2, y2 = x1 + self.cell_size - 30, y1 + self.cell_size - 30
        self.canvas.create_oval(x1, y1, x2, y2, fill="brown", tags="dust")

    def draw_vacuum(self):
        """Draws the vacuum cleaner at its current position."""
        self.canvas.delete("vacuum")
        x, y = self.vacuum_position
        x1, y1 = x * self.cell_size + 10, y * self.cell_size + 10
        x2, y2 = x1 + self.cell_size - 20, y1 + self.cell_size - 20
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="vacuum")

    def move_vacuum(self, direction):
        """Moves the vacuum cleaner in the specified direction."""
        if not self.is_running:
            return

        x, y = self.vacuum_position
        if direction == "up" and y > 0:
            y -= 1
        elif direction == "down" and y < self.grid_size - 1:
            y += 1
        elif direction == "left" and x > 0:
            x -= 1
        elif direction == "right" and x < self.grid_size - 1:
            x += 1

        self.vacuum_position = (x, y)
        self.clean_position()
        self.update_canvas()

    def clean_position(self):
        """Cleans the current position of the vacuum cleaner."""
        if self.vacuum_position in self.dust_positions:
            self.dust_positions.remove(self.vacuum_position)

    def update_canvas(self):
        """Updates the canvas to reflect changes in positions."""
        self.canvas.delete("dust")
        for dust in self.dust_positions:
            self.draw_dust(*dust)
        self.draw_vacuum()

    def auto_move(self):
        """Automatically moves the vacuum cleaner in random directions."""
        if not self.is_running:
            return

        direction = random.choice(["up", "down", "left", "right"])
        self.move_vacuum(direction)
        self.root.after(500, self.auto_move)  # Schedule the next movement

    def start_cleaning(self):
        """Starts the automatic cleaning process."""
        if not self.is_running:
            self.is_running = True
            self.auto_move()

    def stop_cleaning(self):
        """Stops the automatic cleaning process."""
        self.is_running = False

    def resize_canvas(self, event):
        """Resizes the canvas and redraws the rooms when the window is resized."""
        new_width = event.width
        new_height = event.height
        self.cell_size = min(new_width // self.grid_size, new_height // self.grid_size)
        self.draw_rooms()
        self.update_canvas()

# Create the Tkinter app
root = tk.Tk()
app = VacuumCleanerApp(root)
root.mainloop()
