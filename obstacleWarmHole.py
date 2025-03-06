from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Rectangle, PushMatrix, PopMatrix, Color, Rotate
from kivy.core.image import Image as CoreImage

# WarmHole class represents a visual element that can rotate and display an image, acting as a portal
class WarmHole(Widget):
    warmHole_out = False  # Attribute to link the "out" wormhole with another widget (portal exit)

    def __init__(self, source, is_in, angle, **kwargs):
        # Initialize the base class
        super(WarmHole, self).__init__(**kwargs)
        
        # Store whether the WarmHole is an "in" or "out" portal
        self.is_in = is_in
        # Load the image from the provided source and get its texture
        self.source = source
        self.texture = CoreImage(self.source).texture
        # Store the angle for rotation
        self.angle = angle
        
        # Disable size_hint to use a fixed size for the WarmHole widget
        self.size_hint = (None, None)
        # Set the default size of the WarmHole
        self.size = (60, 100)

        # Draw the graphical components for the WarmHole
        with self.canvas:
            # PushMatrix is used to isolate transformations to this widget
            PushMatrix()
            # Set the color (white in this case)
            Color(1, 1, 1)
            # Apply a rotation transformation using the provided angle
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            # Draw a circular area for the portal (using an Ellipse)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            # Draw the image within the ellipse (using the loaded texture)
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=self.size)
            # Restore the previous matrix state to avoid affecting other widgets
            PopMatrix()
