from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import math

# Class representing a small part of the rock
class RockPart(Widget):
    def __init__(self, size, **kwargs):
        # Initialize the base Widget class and pass the size
        super(RockPart, self).__init__(size=size, **kwargs)
        
        # Draw the rectangle that represents this part of the rock
        with self.canvas:
            # Set the color for the rock part (a shade of gray)
            Color(0.5, 0.5, 0.5)
            # Draw the rectangle at the given position with the given size
            self.rect = Rectangle(pos=self.pos, size=self.size)

    # Update the position and size of the rectangle when the widget moves or resizes
    def update_graphics_pos(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Main Rock class, composed of multiple RockPart widgets
class Rock(Widget):
    def __init__(self, width=70, height=70, part_size=(5, 5), **kwargs):
        # Initialize the base Widget class
        super(Rock, self).__init__(**kwargs)
        
        # Set the overall width and height of the rock
        self.width = width
        self.height = height
        # Set the size of each part of the rock
        self.part_size = part_size
        # List to hold the parts that make up the rock
        self.parts = []
        # Set the radius of the rock (assumed circular shape)
        self.radius = 35
        # Populate the rock with parts
        self.populate_parts()

    # Method to populate the rock with smaller parts (RockPart)
    def populate_parts(self):
        # Clear any previous parts from the rock
        for part in self.parts:
            self.remove_widget(part)
        self.parts.clear()

        # Calculate how many parts fit along the diameter of the rock
        parts_count = int(self.radius * 2 / self.part_size[0])
        # Calculate the starting x and y coordinates (top-left corner of the bounding box)
        offset_x = self.center_x - self.radius
        offset_y = self.center_y - self.radius

        # Loop to generate parts within the circular area
        for i in range(parts_count):
            for j in range(parts_count):
                # Calculate the position of the current part
                x = offset_x + i * self.part_size[0]
                y = offset_y + j * self.part_size[1]
                # Check if the center of the part lies within the circular rock boundary
                if self.is_within_circle(x + self.part_size[0] / 2, y + self.part_size[1] / 2):
                    # Create the part and add it to the rock
                    part = RockPart(pos=(x, y), size=self.part_size)
                    self.parts.append(part)  # Add to the parts list
                    self.add_widget(part)  # Add to the widget tree

    # Method to check if a point is within the circular boundary
    def is_within_circle(self, x, y):
        # Calculate the distance from the center of the circle
        distance = math.sqrt((x - self.center_x) ** 2 + (y - self.center_y) ** 2)
        # Return True if the point is within the circle, considering the radius and part size
        return distance <= self.radius - self.part_size[0] / 2  # Adjust to ensure the full part fits inside the circle
