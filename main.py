from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from customWidget.Card.card import Card 
import constants
from game import GamePage 
from recordPage import RecordPage
from helpPage import HelpPage

# HomePage class for the main menu screen
class HomePage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.initializationPage()  # Initialize the layout and content of the home page

    def on_enter(self, *args):
        # Called when the screen is entered
        return super().on_enter(*args)

    def on_leave(self, *args):
        # Called when the screen is exited
        return super().on_leave(*args)

    # Method to handle button press events and change the screen
    def buttonPress(self, page):
        self.parent.transition = SlideTransition(direction='left')  # Set the transition to slide left
        self.parent.current = page  # Change the screen to the one specified by 'page'

    # Method to initialize the home page layout and add widgets
    def initializationPage(self):
        # Background image
        backImage = Image(source=constants.PATH_BACK, fit_mode='fill')

        # FloatLayout to hold all other widgets
        self.layout = FloatLayout(size_hint=(1, 1), pos_hint={"left": 0, "top": 1})

        # Title image
        title = Image(source=constants.PATH_TITLE, pos_hint={"center_x": 0.5, "top": 0.9}, size_hint=(.6, .1))

        # Labels for student name, course, and professor
        name = Label(text=f'{constants.ALUMN}\r\n{constants.MAT}', pos_hint={"right": .98, "top": 0.95}, halign='right', size_hint=(.1, .1), font_size=20)
        iconUni = Image(source=constants.PATH_UNIPV, pos_hint={"x": .02, "top": 0.95}, size_hint=(.1, .1), fit_mode='contain')
        course = Label(text=f'Course of\r\n{constants.COUSRE_NAME}', pos_hint={"x": .04, "top": 0.15}, size_hint=(.1, .1), font_size=20)
        professor = Label(text=f'Professor:\r\n{constants.PROF_NAME}', pos_hint={"right": .98, "top": 0.15}, halign='right', size_hint=(.1, .1), font_size=20)

        # Cards for "Record", "Play", and "Help" sections
        self.cardRecord = Card(image_path=constants.PATH_RECORD, title='RECORD', font_size=30, pos_hint={"center_x": .2, "center_y": .42}, size_hint=(.13, .27), page='record', bg_color_default=[.78, .76, .55, 1], bg_color_hover=[.94, .90, .41, 1])
        self.cardStart = Card(image_path=constants.PATH_PLAY, title='PLAY', font_size=40, pos_hint={"center_x": .5, "center_y": .42}, size_hint=(.17, .35), page='game', bg_color_default=[.25, .35, .43, 1], bg_color_hover=[.03, .42, .73, 1])
        self.cardHelp = Card(image_path=constants.PATH_HELP, title='HELP', font_size=30, pos_hint={"center_x": .8, "center_y": .42}, size_hint=(.13, .27), page='help', bg_color_default=[.70, .59, .58, 1], bg_color_hover=[.94, .58, .52, 1])

        # Add widgets to the layout
        self.add_widget(backImage)  # Add background image
        self.add_widget(self.layout)  # Add the main layout
        self.layout.add_widget(title)  # Add the title
        self.layout.add_widget(name)  # Add student name label
        self.layout.add_widget(course)  # Add course label
        self.layout.add_widget(professor)  # Add professor label
        self.layout.add_widget(iconUni)  # Add university logo
        self.layout.add_widget(self.cardRecord)  # Add the "Record" button card
        self.layout.add_widget(self.cardStart)  # Add the "Play" button card
        self.layout.add_widget(self.cardHelp)  # Add the "Help" button card
        self.layout.do_layout()  # Apply the layout
        self.canvas.ask_update()  # Request canvas redraw

# Main App class for managing the screens
class MyCanun(App):
    def build(self):
        # Set the window size based on constants
        Window.size = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

        # Create a ScreenManager and add screens to it
        sm = ScreenManager()
        sm.add_widget(HomePage(name="home"))  # Add HomePage screen
        sm.add_widget(GamePage(name="game"))  # Add GamePage screen
        sm.add_widget(RecordPage(name="record"))  # Add RecordPage screen
        sm.add_widget(HelpPage(name="help"))  # Add HelpPage screen

        return sm  # Return the ScreenManager

# Run the app
MyCanun().run()  # Start the app
