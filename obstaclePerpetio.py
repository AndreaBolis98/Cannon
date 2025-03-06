from kivy.graphics import Ellipse, Rectangle, Color
from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout

# The Perpetio class represents an object with an image masked inside a circular area.
class Perpetio(FloatLayout):
    # A property to hold the path of the image source
    source = StringProperty('')

    def __init__(self, source, **kwargs):
        # Initialize the base class (FloatLayout) with any additional arguments
        super(Perpetio, self).__init__(**kwargs)
        self.source = source  # Set the image source provided during initialization
        # Load the texture of the image using CoreImage
        self.texture = CoreImage(self.source).texture
        # Disable size_hint to use fixed size dimensions
        self.size_hint = (None, None)
        # Set the size of the Perpetio object to a default (60x60)
        self.size = (60, 60)

        # Create the graphical elements
        with self.canvas:
            # Set the color to white (this will be applied to the following elements)
            Color(1, 1, 1)
            # Draw a circular mask (stencil) using an Ellipse
            self.circle = Ellipse(pos=self.pos, size=self.size)
            # Draw the image inside the mask using a Rectangle
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=self.size)

        # Bind changes in position and size to update the graphics accordingly
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    # This method updates the position and size of the graphical elements when the widget is resized or moved
    def update_graphics(self, *args):
        # Update the position and size of the rectangle to match the Perpetio widget's current properties
        self.rect.pos = self.pos
        self.rect.size = self.size
