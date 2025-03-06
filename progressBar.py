from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle
import constants

# Custom layout class that triggers an event when touched
class CustomFloatLayout(FloatLayout):
    def on_touch_down(self, touch):
        # Check if the touch is within the layout's bounds
        if self.collide_point(*touch.pos):
            # Dispatch a custom event
            self.dispatch('on_layout_press', touch)
        # Call the default touch down behavior
        return super().on_touch_down(touch)

    def on_layout_press(self, touch):
        # Trigger parent event or custom behavior when the layout is pressed
        self.parent.parent.on_layout_press(touch)
        pass

    # Initialization and registering a custom event type
    def __init__(self, **kwargs):
        # Register the custom event 'on_layout_press'
        self.register_event_type('on_layout_press')
        super(CustomFloatLayout, self).__init__(**kwargs)


# Custom ProgressBar class with an icon and custom graphics
class CustomProgressBar(BoxLayout):
    def __init__(self, **kwargs):
        # Initialize BoxLayout with a horizontal orientation
        super(CustomProgressBar, self).__init__(orientation='horizontal', **kwargs)
        self.spacing = 20  # Set spacing between widgets

        # Add an icon (image) to the left of the progress bar
        self.icon = Image(source=constants.PATH_POWER, size_hint=(0.15, 1))
        self.add_widget(self.icon)

        # Create a container for the progress bar (using FloatLayout for flexibility)
        self.progress_container = FloatLayout(size_hint=(1, 0.8), pos_hint={'top': 0.9})
        self.add_widget(self.progress_container)

        # Draw the progress bar background and border
        with self.progress_container.canvas.before:
            # Grey border for the progress bar
            self.border_color = Color(0.6, 0.6, 0.6, 1)
            self.border_rect = RoundedRectangle(
                size=(self.progress_container.width + 8, self.progress_container.height + 8),
                pos=(self.progress_container.x - 4, self.progress_container.y - 4),
                radius=[15]
            )

            # Light grey background for the progress bar
            self.bg_color = Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = RoundedRectangle(
                size=self.progress_container.size,
                pos=self.progress_container.pos,
                radius=[15]
            )
        
        # Draw the progress bar itself (red color)
        with self.progress_container.canvas:
            self.progress_color = Color(1, 0.4, 0.4, 1)  # Red progress color
            self.progress_rect = RoundedRectangle(
                size=(0, self.progress_container.height * 0.9),  # Start with 0 width
                pos=self.progress_container.pos,
                radius=[15]
            )

        # Bind size and position changes to update the progress bar graphics
        self.progress_container.bind(size=self.update_rect, pos=self.update_rect)

        # Create the ProgressBar widget to manage the actual progress value
        self.progress_bar = ProgressBar(max=100, value=0)
        self.progress_bar.bind(value=self.update_progress)

    # Method to update the background and border when the container is resized or moved
    def update_rect(self, *args):
        self.bg_rect.size = self.progress_container.size
        self.bg_rect.pos = self.progress_container.pos

        self.border_rect.size = (self.progress_container.width + 4, self.progress_container.height + 4)
        self.border_rect.pos = (self.progress_container.x - 2, self.progress_container.y - 2)

        # Call update_progress to adjust the progress bar size
        self.update_progress()

    # Method to update the progress bar size based on the current value
    def update_progress(self, *args):
        # Calculate the width of the progress based on the current value
        progress_width = (self.progress_bar.value / self.progress_bar.max) * self.progress_container.width
        # Update the size and position of the progress rectangle
        self.progress_rect.size = (progress_width, self.progress_container.height)
        self.progress_rect.pos = self.progress_container.pos

    # Method to manually set the progress value
    def set_value(self, value):
        self.progress_bar.value = value  # Update the value of the progress bar
