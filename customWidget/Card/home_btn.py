from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

# Define an IconButton class that combines ButtonBehavior and Image
class IconButton(ButtonBehavior, Image):
    def __init__(self, source, page, **kwargs):
        # Initialize the ButtonBehavior and Image classes
        super(IconButton, self).__init__(**kwargs)
        
        self.source = source  # Set the image source for the icon
        self.page = page  # Store the page that will be triggered on click
        
        self.size_hint = (None, None)  # Disable size_hint to use fixed size
        self.size = (100, 100)  # Set a fixed size for the icon (100x100)
    
    # Called when the button is released (clicked)
    def on_release(self):
        # Trigger an action when the button is clicked
        # Assuming `homebtn` is a method in the parent's parent (perhaps for navigation)
        self.parent.parent.parent.homebtn(self.page)
        return super().on_release()  # Call the parent class's on_release method
