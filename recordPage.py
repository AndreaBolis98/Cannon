from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from customWidget.Card.home_btn import IconButton
import constants
import saveResult

# RecordPage class for displaying the Hall of Fame screen with high scores
class RecordPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # Called when the screen is entered
    def on_enter(self):
        super().on_enter()
        # Load the scores from the saved results
        self.score = saveResult.readResult()
        # Initialize the page layout
        self.initializationaPage()

    # Called when the screen is left
    def on_leave(self):
        super().on_leave()
        # Clear the widgets to reset the layout
        self.clear_widgets()

    # Navigate to the home page
    def homebtn(self, page):
        self.parent.current = page

    # Method to initialize the layout and populate the Hall of Fame
    def initializationaPage(self):
        # Icon button for navigating back to the home page
        iconbtn = IconButton(constants.PATH_HOME, 'home', pos_hint={'x': 0, 'top': 1})
        
        # Background image for the screen
        backImage = Image(source=constants.PATH_BACK, fit_mode='fill')

        # Main layout (vertical box layout)
        gridLayout = BoxLayout(orientation='vertical')

        # Header section in a FloatLayout
        floatLayout = FloatLayout(size_hint=(1, .25))
        header = Label(
            text="HALL OF FAME",
            font_size=50,
            font_name=constants.PIXEL_REGULAR,
            pos_hint={"center_x": 0.5, "center_y": .5},
            size_hint=(1, 1)
        )

        # Scrollable section to display the list of scores
        tabScore = ScrollView(do_scroll_x=False, size_hint=(1, .75), pos_hint={'top': 0.75})
        self.gridScore = BoxLayout(spacing=12, orientation='vertical', size_hint_y=None, height=500)
        
        # Bind the minimum height to the height of the score grid, allowing it to grow as scores are added
        self.gridScore.bind(minimum_height=self.gridScore.setter('height'))

        # Add all the widgets to the layout
        self.add_widget(backImage)  # Add background
        self.add_widget(gridLayout)  # Add main layout
        gridLayout.add_widget(floatLayout)  # Add header layout
        gridLayout.add_widget(tabScore)  # Add the score table (ScrollView)
        tabScore.add_widget(self.gridScore)  # Add the score grid inside the scroll view
        floatLayout.add_widget(iconbtn)  # Add the home button
        floatLayout.add_widget(header)  # Add the header text
        
        # Populate the Hall of Fame with scores
        self.popolate_tab()

    # Method to populate the score table
    def popolate_tab(self):
        i = 1  # Position counter for ranking

        # Loop through the score list and add each score to the table
        for rec in self.score:
            # Create a RowTable widget for each score with the name, score, and position
            stringScore = RowTable(name=rec['name'], score=rec['score'], position=i)
            # Add the row to the score grid
            self.gridScore.add_widget(stringScore)
            i += 1  # Increment position for the next row

# RowTable class for representing a row in the score table
class RowTable(BoxLayout):
    # Default colors for the background and border of the row
    border_color = (.13, .20, .30, .8)
    bg_color = (.13, .20, .30, .7)

    def __init__(self, name, score, position, **kwargs):
        super(RowTable, self).__init__(**kwargs)
        self.padding = [10, 10, 10, 10]  # Padding around the content inside the row
        self.size_hint = (.9, None)  # Fixed width for the row
        self.height = 60  # Fixed height for the row

        # Set the source for the ranking icons based on the position
        if position == 1:
            source = constants.PATH_STAR_GOLD
        elif position == 2:
            source = constants.PATH_STAR_SILVER
        elif position == 3:
            source = constants.PATH_STAR_BRONZE

        # If the position is 1, 2, or 3, display an image icon for the rank
        if position <= 3:
            classification = Image(source=source)
        else:
            # For positions greater than 3, display the rank as a number
            classification = Label(text=f'{position}', font_size=40, font_name=constants.PIXEL_REGULAR)

        # Label for the player's name
        name = Label(text=f'NAME: {name}', font_size=40, font_name=constants.PIXEL_REGULAR)
        # Label for the player's score
        score = Label(text=f'SCORE: {score}', font_size=40, font_name=constants.PIXEL_REGULAR)

        # Add the ranking icon/number, player name, and score to the row
        self.add_widget(classification)
        self.add_widget(name)
        self.add_widget(score)
