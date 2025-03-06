from kivy.uix.image import Image
from kivy.animation import Animation
import constants

# Target class representing a target object on the screen
class Target(Image):
    def __init__(self, **kwargs):
        super(Target, self).__init__(**kwargs)
        
        # Calculate the pixel size based on the screen size and aspect ratio
        pix_y = constants.SCREEN_HEIGHT * self.size_hint_y
        pix_x = pix_y * 0.7  # Maintain the aspect ratio (width to height ratio of 0.7)
        
        # Set the width of the target based on its height
        self.size_hint_x = (pix_x / constants.SCREEN_WIDTH)

    # Method to be called when the target is hit
    def is_hit(self):
        # Define the first animation: move the target down to a position near the bottom of the screen
        animation1 = Animation(pos_hint={'y': 0.1}, duration=1)
        
        # Define the second animation: move the target completely off the screen
        animation2 = Animation(pos_hint={'y': -1}, duration=1)
        
        # Chain the animations: once the first animation is complete, start the second animation
        animation1.bind(on_complete=lambda *args: animation2.start(self))
        
        # After the second animation completes, update the level in the game
        animation2.bind(on_complete=lambda *args: self.parent.parent.parent.updateLevel(0))
        
        # Start the first animation
        animation1.start(self)
