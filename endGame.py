from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from customWidget.Card.card import Card 
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
import constants
import saveResult

class TransparentOverlay(BoxLayout):
    level = 0  # Current game level
    points = 0  # Points scored by the player
    count = [0, 0, 0]  # Placeholder for counters

    def __init__(self, **kwargs):
        # Extract keyword arguments and set properties
        self.count = kwargs.pop('count', None)
        self.level = kwargs.pop('level', None)
        self.points = kwargs.pop('points', None)
        self.pos = kwargs.pop('pos', None)
        self.size = kwargs.pop('size', None)
        self.win = kwargs.pop('win', None)

        super(TransparentOverlay, self).__init__(**kwargs)
        self.orientation = 'vertical'  # Set orientation to vertical
        
        # Create a semi-transparent background overlay
        with self.canvas:
            Color(0, 0, 0, 0.5)  # Black color with 50% opacity
            self.rect = Rectangle(pos=self.pos, size=self.size)  # Rectangle to cover the entire window

        # Set up the overlay page with relevant labels and inputs
        self.set_page(self.win)

    def set_page(self, win):
        # Define a win or game over message
        if win:
            message = f"[b][color=00ff00]YOU WIN[/color][/b]"  # Green for winning
        else:
            message = f"[b][color=ff0000]GAME OVER[/color][/b]"  # Red for game over

        # Create an overlay label showing the win/game over message
        overlay_label = Label(
            text=message,
            font_size='80sp',
            font_name=constants.PIXEL_REGULAR,
            markup=True  # Allow markup for font color and bold
        )

        # Display the current level
        level_label = Label(
            text=f'[color=ffffff]LEVEL:[/color] [color=00ff00]{self.level}[/color]',  # Level text in green
            font_size='40sp',
            font_name=constants.PIXEL_REGULAR,
            markup=True
        )

        # Label to show the player's current score
        self.points_label = Label(
            text=f'[color=ffffff]HI:[/color] [color=00ff00]{self.points}[/color]',  # Points text in green
            font_size='40sp',
            font_name=constants.PIXEL_REGULAR,
            markup=True
        )

        # Create an empty widget for classification or ranking
        self.classification = Widget()

        # Label for the Hall of Fame section
        labelHallOfFame = Label(
            text='Hall of fame:',
            font_size='40sp',
            font_name=constants.PIXEL_REGULAR,
            markup=True
        )

        # Text input for entering the player's name
        self.text_input = TextInput(
            hint_text='Enter your name here',
            font_size=25,
            multiline=False,  # Single-line input
            size_hint=(1, 0.5),  # Take up 50% of the height
            pos_hint={'center_x': .5, "center_y": .5}  # Center the text input
        )

        # Create layout rows
        secondRow = BoxLayout(orientation="horizontal")
        thirdRow = BoxLayout(orientation="horizontal")
        secondAndThird = BoxLayout(orientation="vertical", padding=[100, 0, 100, 0])
        self.hallOfFameBox = BoxLayout(orientation="horizontal")

        # Add the overlay label and layout rows to the widget
        self.add_widget(overlay_label)
        self.add_widget(secondAndThird)
        secondAndThird.add_widget(secondRow)
        secondAndThird.add_widget(thirdRow)

        # Add level label and Hall of Fame box to the second row
        secondRow.add_widget(level_label)
        secondRow.add_widget(self.hallOfFameBox)

        # Add points label and text input to the third row
        thirdRow.add_widget(self.points_label)
        thirdRow.add_widget(self.text_input)

        # Add the Hall of Fame label and classification widget
        self.hallOfFameBox.add_widget(labelHallOfFame)
        self.hallOfFameBox.add_widget(self.classification)

    def update_points(self, inc):
        # Update the points and refresh the points label
        self.points += inc
        self.points_label.text = f'[color=ffffff]LEVEL:[/color] [color=00ff00]{self.points}[/color]'
        # Update the Hall of Fame classification
        self.get_classification()

    def get_classification(self):
        # Check the result and get the classification (ranking)
        positionScore = saveResult.checkResult(self.text_input.text, self.points)

        # Set the correct image based on position in the Hall of Fame
        if positionScore == 1:
            source = constants.PATH_STAR_GOLD
        elif positionScore == 2:
            source = constants.PATH_STAR_SILVER
        elif positionScore == 3:
            source = constants.PATH_STAR_BRONZE

        # Clear the previous classification widget
        self.hallOfFameBox.remove_widget(self.classification)

        # Display the appropriate image or rank based on position
        if positionScore <= 3:
            self.classification = Image(source=source, size_hint=(.5, .3), pos_hint={'center_x': .5, 'center_y': .5})
        else:
            self.classification = Label(text=f'{positionScore}', font_size=40, font_name=constants.PIXEL_REGULAR)

        # Add the classification widget back to the layout
        self.hallOfFameBox.add_widget(self.classification)

    def add_exit(self):
        # Create an exit layout with buttons for home and save
        boxExit = BoxLayout(orientation='horizontal', padding=[500, 0, 500, 0], spacing=20)

        # Home button card
        cardHome = Card(
            image_path=constants.PATH_HOME, 
            title='HOME', 
            font_size=20, 
            pos_hint={"center_x": .5, "center_y": .5}, 
            size_hint=(.2, .5), 
            page='home', 
            bg_color_default=[.25, .35, .43, 1], 
            bg_color_hover=[.03, .42, .73, 1]
        )

        # Save button card
        cardSave = Card(
            image_path=constants.PATH_SAVE, 
            title='SAVE', 
            font_size=20, 
            pos_hint={"center_x": .5, "center_y": .5}, 
            size_hint=(.2, .5), 
            page='save', 
            bg_color_default=[.78, .76, .55, 1], 
            bg_color_hover=[.94, .90, .41, 1]
        )

        # Add exit layout and buttons to the widget
        self.add_widget(boxExit)
        boxExit.add_widget(cardHome)
        boxExit.add_widget(cardSave)

    # Method to handle button press events and change the screen
    def buttonPress(self, page):
        # Handle saving the game and navigating home
        if page == 'save':
            saveResult.saveResult(self.text_input.text, self.points)  # Save the result
            page = 'home'
            self.parent.parent.parent.parent.current = page  # Navigate home
        elif page == 'home':
            self.parent.parent.parent.homebtn(page)  # Go to the home screen
