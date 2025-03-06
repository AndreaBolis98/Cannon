from kivy.uix.widget import Widget
from kivy.graphics import Rotate, PushMatrix, PopMatrix, Color, Rectangle
from kivy.properties import NumericProperty

# Mirror class representing a mirror widget with a specific rotation angle
class Mirror(Widget):
    # Angle property that allows dynamic changes to the rotation of the mirror
    angle = NumericProperty(0)  
    
    def __init__(self, **kwargs):
        # Set default size of the mirror if not provided in kwargs
        size = kwargs.pop('size', (10, 100))  
        # Get the rotation angle from kwargs, default is 0 degrees
        self.angle = kwargs.pop('angle', 0)  
        
        # Initialize the base Widget class
        super(Mirror, self).__init__(**kwargs)
        
        # Set the size of the mirror to the provided or default size
        self.size = size  
        # Disable size_hint to allow using fixed size dimensions
        self.size_hint = (None, None)  
        
        # Create and apply graphical transformations and visual elements to the widget
        with self.canvas:
            PushMatrix()  # Save the current graphics matrix
            Color(.4, .83, .9)  # Set the color of the mirror (green in this case)
            # Apply a rotation to the mirror widget
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            # Draw the rectangular shape of the mirror
            self.mirror_rect = Rectangle(pos=self.pos, size=self.size)
            PopMatrix()  # Restore the previous graphics matrix
        
        # Bind position and size changes to update the mirror's graphics
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    # Method to update the mirror's graphics when its position or size changes
    def update_graphics(self, *args):
        # Update the position and size of the rectangle representing the mirror
        self.mirror_rect.pos = self.pos
        self.mirror_rect.size = self.size
        # Update the origin of the rotation to the center of the mirror
        self.rotation.origin = self.center
