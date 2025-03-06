from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from customWidget.Card.hover_behavior import HoverBehavior
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ColorProperty

import os
import sys
# Adds the current working directory to the system path
sys.path.insert(1, os.getcwd())
from constants import * 

# Define the UI structure of the CardAmmunition widget using Kivy's Builder syntax
Builder.load_string('''
<CardAmmunition>:
    padding: [10, 10, 10, 10]  # Padding around the content inside the card
    size_hint: None, None  # Disable automatic resizing
    size: self.minimum_size  # Ensure size is based on content
    canvas.before:
        Color:
            rgba:  root.border_color  # Use border color from root properties
        Line:
            rounded_rectangle: (self.x + 1, self.y + 1, self.width - 2, self.height - 2, 15)  # Draw rounded border
            width: 1.5
        Color:
            rgba: root.bg_color  # Set background color from root properties
        RoundedRectangle:
            pos: self.pos  # Position background rectangle based on widget's position
            size: self.size  # Size background rectangle to match widget's size
            radius: [15]  # Set corner radius for rounded effect
    BoxLayout:
        orientation: 'vertical'  # Arrange elements vertically
        Label:
            id: card_label  # Label for the card's title
            text: root.title  # Text is linked to the widget's title property
            size_hint_y: None  # Disable vertical resizing
            font_size: root.font_size  # Set font size from root property
            font_name: root.font_name  # Set font name from root property
            height: self.texture_size[1]  # Set height to fit text content
            text_size: self.width, None  # Constrain text width to label width
            halign: 'center'  # Center the text horizontally
            valign: 'middle'  # Center the text vertically
        Image:
            id: card_image  # Image to display in the card
            source: root.image_path  # Set image source from root's image_path property
        Label:
            id: card_count  # Label for the ammunition count
            text: root.count  # Text is linked to the widget's count property
            size_hint_y: None  # Disable vertical resizing
            font_size: root.font_size  # Set font size from root property
            font_name: root.font_name  # Set font name from root property
            height: self.texture_size[1]  # Set height to fit text content
            text_size: self.width, None  # Constrain text width to label width
            halign: 'center'  # Center the text horizontally
''')

# CardAmmunition class that inherits from BoxLayout, HoverBehavior, and Button
class CardAmmunition(BoxLayout, HoverBehavior, Button):
    image_path = StringProperty('')  # Path to the image displayed on the card
    title = StringProperty('Text')  # Title text displayed on the card
    index = NumericProperty(0)  # Index to identify the card
    count = StringProperty(0)  # Ammunition count displayed on the card
    font_name = PIXEL_REGULAR  # Default font for the card text
    font_size = 20  # Default font size
    border_color = ColorProperty([.13, .20, .30, .8])  # Default border color
    bg_color = ColorProperty([.13, .20, .30, .7])  # Default background color

    def __init__(self, index, **kwargs):
        super(CardAmmunition, self).__init__(**kwargs)
        self.index = index  # Set the index for this card
        self.background_color = ([0, 0, 0, 0])  # Set the background to transparent
        self.ids.card_image.source = self.image_path  # Set the image source for the card
        self.updateColor(0)  # Initialize the card color

    def post_init(self, instance, value):
        # This method is called after initialization to update the card color
        if value:
            self.updateColor(0)

    def updateColor(self, val):
        # Update the border and background color based on the selected index
        if self.index == val:
            # If this card is selected, change its color to white
            self.border_color = ([1, 1, 1, 1])
            self.bg_color = ([1, 1, 1, .7])
        else:
            # Otherwise, use the default colors
            self.border_color = ([.13, .20, .30, .8])  
            self.bg_color = ([.13, .20, .30, .7])

    def on_press(self):
        # Called when the card is pressed
        # Change the muzzle in the parent cannon object to the current index
        self.parent.parent.parent.parent.cannon.change_muzzle(self.index)
        return super().on_press()
