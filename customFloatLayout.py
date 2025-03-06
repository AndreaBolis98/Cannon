from kivy.uix.floatlayout import FloatLayout

# Define a custom FloatLayout class that can handle custom touch events
class CustomFloatLayout(FloatLayout):
    
    # Override the on_touch_down method to handle touch events
    def on_touch_down(self, touch):
        # Check if the touch point is within the widget's bounds
        if self.collide_point(*touch.pos):
            # If it is, trigger a custom event (on_layout_press)
            self.dispatch('on_layout_press', touch)
        # Call the base class method to ensure normal touch handling continues
        return super().on_touch_down(touch)

    # Define the custom event handler for 'on_layout_press'
    def on_layout_press(self, touch):
        # When this event is triggered, it calls the touch_down method on the parent of the parent
        self.parent.parent.touch_down()

    # Constructor to initialize the widget
    def __init__(self, **kwargs):
        # Register the custom event type 'on_layout_press'
        self.register_event_type('on_layout_press')
        # Call the base class constructor to complete initialization
        super(CustomFloatLayout, self).__init__(**kwargs)
