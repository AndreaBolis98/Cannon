from kivy.properties import BooleanProperty
from kivy.core.window import Window

# HoverBehavior class to detect when the mouse hovers over a widget
class HoverBehavior(object):
    hovered = BooleanProperty(False)  # Tracks whether the mouse is hovering over the widget
    border_point = None  # Optional property for storing the hover boundary (not currently used)

    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        self._bind_mouse()  # Bind the mouse position event to track hover behavior

    # Bind the mouse position to the widget's on_mouse_pos method
    def _bind_mouse(self):
        Window.bind(mouse_pos=self.on_mouse_pos)

    # Check the mouse position relative to the widget and update the hovered state
    def on_mouse_pos(self, *args):
        pos = args[1]  # Get the mouse position from the arguments
        # Check if the mouse is inside the widget
        inside = self.collide_point(*self.to_widget(*pos))
        # If the hover state hasn't changed, return
        if self.hovered == inside:
            return
        # Update the hovered property to match the new hover state
        self.hovered = inside
        # Trigger the appropriate event when the mouse enters or leaves the widget
        if inside:
            self.on_mouse_enter()
        else:
            self.on_mouse_leave()

    # Method to be called when the mouse enters the widget (to be overridden in subclasses)
    def on_mouse_enter(self):
        pass

    # Method to be called when the mouse leaves the widget (to be overridden in subclasses)
    def on_mouse_leave(self):
        pass

    # Override touch behavior to ensure it only processes touch when hovered
    def on_touch_down(self, touch):
        if self.hovered:  # Only process touch events if the widget is being hovered
            return super(HoverBehavior, self).on_touch_down(touch)
        return False  # Ignore touch events when not hovered
