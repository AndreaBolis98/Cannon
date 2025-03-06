from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from customWidget.Card.hover_behavior import HoverBehavior
from kivy.properties import StringProperty, NumericProperty, ColorProperty

import os
import sys
# Adds the current working directory to the system path
sys.path.insert(1, os.getcwd())
from constants import PIXEL_REGULAR

# Kivy Builder string defining the UI layout of the Card widget
Builder.load_string('''
<Card>:
    padding: [10, 10, 10, 10]  # Padding around the content inside the card
    size_hint: None, None  # Disable automatic size adjustments
    size: self.minimum_size  # Ensure the size is based on content
    canvas.before:
        Color:
            rgba: root.bg_color  # Set the background color from the root's bg_color property
        RoundedRectangle:
            pos: self.pos  # Set position of the background rectangle
            size: self.size  # Set size of the background rectangle
            radius: [30]  # Make the corners of the background rectangle rounded
    BoxLayout:
        orientation: 'vertical'  # Arrange children vertically inside the card
        Label:
            id: card_label  # Label widget for the title of the card
            text: root.title  # Bind label text to the card's title property
            font_size: root.font_size  # Set the font size from the card's property
            color: root.font_color  # Set font color from the card's property
            font_name: root.font_name  # Set font name from the card's property
            size_hint_y: None  # Disable vertical resizing for the label
            height: self.texture_size[1]  # Set the label height based on the text size
            text_size: self.width, None  # Constrain text width to label's width
            halign: 'center'  # Center-align the text horizontally
            valign: 'middle'  # Center-align the text vertically
        Image:
            id: card_image  # Image widget to display an image in the card
            source: root.image_path  # Bind image source to the card's image_path property
''')

# Define the Card class, which inherits from BoxLayout, HoverBehavior, and Button
class Card(BoxLayout, HoverBehavior, Button):
    # Properties for the card's visual appearance and content
    image_path = StringProperty('')  # Path to the image to display in the card
    title = StringProperty('Text')  # Title text for the card
    font_color = ColorProperty([1, 1, 1, 1])  # Default font color (white)
    font_name = StringProperty(PIXEL_REGULAR)  # Default font style
    font_size = NumericProperty(0)  # Font size for the title text
    bg_color = ColorProperty([0, 0, 0, 0])  # Background color of the card
    bg_color_default = ColorProperty([1, 1, 1, 0])  # Default background color (transparent)
    bg_color_hover = ColorProperty([1, 1, 1, 0])  # Background color when the mouse hovers over the card
    
    # Constructor to initialize the card with default values or user-provided values
    def __init__(self, image_path='', title='Text', font_size=30, pos_hint=None, size_hint=(None, None), page=None, bg_color_default=None, bg_color_hover=None, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.background_color = [1, 1, 1, 0]  # Set the background color to transparent
        self.image_path = image_path  # Set the image path for the card
        self.title = title  # Set the title for the card
        self.font_size = font_size  # Set the font size for the title
        self.pos_hint = pos_hint  # Set position hint if provided
        self.size_hint = size_hint  # Set size hint if provided
        self.page = page  # Optional page reference for navigation
        self.bg_color_default = bg_color_default if bg_color_default else [1, 1, 1, 0]  # Set default background color
        self.bg_color_hover = bg_color_hover if bg_color_hover else [1, 1, 1, 0]  # Set hover background color
        self.bg_color = self.bg_color_default  # Initialize background color with default value

    # Method called after initialization, sets the image source
    def post_init(self, instance, value):
        if value:
            self.ids.card_image.source = self.image_path  # Set the image source after initialization

    # Event handler for when the mouse enters the widget (hover effect)
    def on_mouse_enter(self):
        self.size_hint = (self.size_hint[0] * 1.2, self.size_hint[1] * 1.2)  # Enlarge the widget
        self.font_size *= 1.2  # Increase font size proportionally
        self.bg_color = self.bg_color_hover  # Change background color to hover color

    # Event handler for when the mouse leaves the widget (reverting hover effect)
    def on_mouse_leave(self):
        self.size_hint = (self.size_hint[0] / 1.2, self.size_hint[1] / 1.2)  # Restore original size
        self.font_size /= 1.2  # Restore the original font size
        self.bg_color = self.bg_color_default  # Restore the default background color
    
    # Event handler for when the card is clicked
    def on_release(self):
        if self.page:
            # If a page is set, trigger navigation to the page (this example assumes a parent method `buttonPress`)
            self.parent.parent.buttonPress(self.page)
        return super().on_release()  # Call the base class' on_release method
