from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty

import os
import sys
# Insert root directory into Python module search path
sys.path.insert(1, os.getcwd())
from constants import *  # Assuming PIXEL_REGULAR is imported from constants

# Load the Kivy layout using the Builder
Builder.load_string('''
<RecordCard>:
    padding: [10, 10, 10, 10]  # Padding around the content inside the card
    size_hint: None, None  # Disable size_hint for fixed size layout
    size: self.minimum_size  # Size is based on the content inside
    BoxLayout:
        orientation: 'vertical'  # Arrange widgets vertically
        Image:
            id: card_image  # Image widget to display an image
            source: root.image_path  # Image source is bound to the image_path property
            pos_hint: {"center_x": 0.5, "top": 1}  # Center the image horizontally and align to the top
        Label:
            id: card_label  # Label widget to display the title
            text: root.title  # Text is bound to the title property
            font_size: root.font_size  # Font size is set from the font_size property
            font_name: root.font_name  # Font name is set from the font_name property
            size_hint_y: None  # Disable vertical resizing for the label
            height: self.texture_size[1]  # Set height based on text content
            text_size: self.width, None  # Constrain text width to label's width
            halign: 'center'  # Center-align the text horizontally
            valign: 'middle'  # Center-align the text vertically
''')

# Define the RecordCard class
class RecordCard(BoxLayout):
    # Define properties for the card's content and appearance
    image_path = StringProperty('')  # Path to the image displayed on the card
    title = StringProperty('Text')  # Title displayed on the card
    font_name = PIXEL_REGULAR  # Default font name, assumed to be imported from constants
    font_size = 30  # Default font size
    background_color = ListProperty([1, 1, 1, 0])  # Default background color (transparent)
    background_color_down = ListProperty([1, 1, 1, 0])  # Background color when pressed

    def __init__(self, **kwargs):
        super(RecordCard, self).__init__(**kwargs)
        # Store the original size hint for restoring the widget's size
        self.original_size = self.size_hint

    # Called after initialization to update the image source
    def post_init(self, instance, value):
        if value:
            self.ids.card_image.source = self.image_path  # Set the image source after initialization
