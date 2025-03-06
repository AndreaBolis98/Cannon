from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from customWidget.Card.home_btn import IconButton
from kivy.graphics import Color, RoundedRectangle
import constants

# HelpPage class provides detailed instructions to the user about the game mechanics
class HelpPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # This method is called when the screen is entered
    def on_enter(self):
        super().on_enter()  # Call the parent method
        self.initializationaPage()  # Initialize the page layout and content

    # This method is called when leaving the screen
    def on_leave(self):
        super().on_leave()  # Call the parent method
        self.clear_widgets()  # Clear the widgets when leaving the page

    # Method to handle home button press, navigates to the home page
    def homebtn(self, page):
        self.parent.current = page  # Change the screen to the given page (home)

    # PAGE OBJECTS

    # Initialize the layout and content of the HelpPage
    def initializationaPage(self):
        # Create a home button that allows users to return to the home page
        iconbtn = IconButton(constants.PATH_HOME, 'home', pos_hint={'x': 0, 'top': 1})

        # Set up the background image
        backImage = Image(source=constants.PATH_BACK, fit_mode='fill')

        # Create a vertical layout for the help content
        gridLayout = BoxLayout(orientation='vertical')

        # Create a floating layout for the header and home button
        floatLayout = FloatLayout(size_hint=(1, .25))

        # Create the header label
        header = Label(
            text="HELP CENTER", 
            font_size=50, 
            font_name=constants.PIXEL_REGULAR, 
            pos_hint={"center_x": 0.5, "center_y": .5}, 
            size_hint=(1, 1)
        )

        # Create a horizontal layout for the help sections
        self.gridHelp = BoxLayout(orientation='horizontal', spacing=30, padding=30)

        # Add the background and layouts to the screen
        self.add_widget(backImage)
        self.add_widget(gridLayout)
        gridLayout.add_widget(floatLayout)
        gridLayout.add_widget(self.gridHelp)
        floatLayout.add_widget(iconbtn)  # Add the home button to the floating layout
        floatLayout.add_widget(header)  # Add the header label to the floating layout

        # Call the method to set up the help content
        self.fire()

    # This method adds sections to the help page
    def fire(self):
        layoutFire = MyBoxLayout()  # Create a layout for the "How to Fire the Cannon" section
        layoutLevel = MyBoxLayout()  # Create a layout for the "Levels and Obstacles" section

        # Add both layouts to the main help grid
        self.gridHelp.add_widget(layoutFire)
        self.gridHelp.add_widget(layoutLevel)

        # Add "How to Fire the Cannon" help content
        titleFire = Label(
            text=f"[b][color=ff0000]How to Fire the Cannon[/color][/b]",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=1,
            size_hint_y=.1,
            pos_hint={'x': 0},
            markup=True
        )
        firstRow = Label(
            text="The cannon is your main weapon in the game. \nHere’s how to use it effectively",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=1,
            pos_hint={'x': 0},
            markup=True
        )
        secondtRow = Label(
            text="Aiming: \nUse the mouse to aim the cannon at your target.",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=1,
            pos_hint={'x': 0},
            markup=True
        )
        thirdRow = Label(
            text="Choosing Your Weapon: \nYou can choose different types of weapons: projectile, bomb, and\nlaser. Each weapon has unique characteristics and can be\nselected based on your strategy.",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=1,
            pos_hint={'x': 0},
            markup=True
        )
        fourthRow = Label(
            text="Charging and Releasing the Shot:\nHold down the left mouse button to start charging the shot.\nWatch the charging bar that is above the cannon. When the charging bar\nis full or reaches the desired power, release the mouse button to\nfire. The fuller the bar, the more powerful the shot will be.",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=1,
            pos_hint={'x': 0},
            markup=True
        )

        # Add the help content to the layout
        layoutFire.add_widget(titleFire)
        layoutFire.add_widget(firstRow)
        layoutFire.add_widget(secondtRow)
        layoutFire.add_widget(thirdRow)
        layoutFire.add_widget(fourthRow)

        # Add "Levels and Obstacles" help content
        titleLevel = Label(
            text=f"[b][color=ff0000]Levels and Obstacles[/color][/b]",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=1,
            size_hint_y=.1,
            pos_hint={'x': 0},
            markup=True
        )
        
        # Create specific obstacle descriptions with images
        firstRowLevel = BoxLayoutLevel(source=constants.PATH_ROCK, label="This obstacle crumbles with each hit,\nrequiring multiple attacks to be eliminated")
        secondtRowLevel = BoxLayoutLevel(source=constants.PATH_PERPETIO, label="Indestructible by any projectile. No weapon can damage it")
        thirdRowLevel = BoxLayoutLevel(source=constants.PATH_MIRROR, label="Reflects laser pulses, cannot be destroyed by any weapon")
        fourthRowLevel = BoxLayoutLevel(source=constants.PATH_WARMHOLE_IN, label="When a projectile hits one of the two elements of the wormhole,\nit continues its trajectory out of the other element")

        # Information about scoring and points
        fifthRowLevel = Label(
            text=f"Once you pass a level, the points will increase by {constants.LEVEL_POINT} points",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=1,
            pos_hint={'x': 0},
            markup=True
        )
        
        # Cost of each type of shot
        sixthRowLevel = Label(
            text=f"Every shot has a cost in terms of points:\n - BULLET: {constants.AMMU_POINTS[0]}\n - BOMB: {constants.AMMU_POINTS[1]}\n - LASER: :{constants.AMMU_POINTS[2]}\n",
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='center',
            valign='top',
            size_hint_x=1,
            pos_hint={'x': 0},
            markup=True
        )

        # Add the obstacle descriptions and information to the layout
        layoutLevel.add_widget(titleLevel)
        layoutLevel.add_widget(firstRowLevel)
        layoutLevel.add_widget(secondtRowLevel)
        layoutLevel.add_widget(thirdRowLevel)
        layoutLevel.add_widget(fourthRowLevel)
        layoutLevel.add_widget(fifthRowLevel)
        layoutLevel.add_widget(sixthRowLevel)

# Custom BoxLayout with a semi-transparent background
class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'  # Set layout orientation to vertical
        self.padding = 20  # Set padding inside the layout
        self.spacing = 20  # Set spacing between elements

        # Draw a semi-transparent rectangle background
        with self.canvas.before:
            Color(.13, .20, .30, .7)  # Set the background color with transparency
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

        # Bind the layout's position and size to the rectangle to update dynamically
        self.bind(pos=self.update_shapes, size=self.update_shapes)

    # Update the rectangle's size and position when the layout is resized or moved
    def update_shapes(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# A custom BoxLayout used for level descriptions with images and labels
class BoxLayoutLevel(BoxLayout):
    def __init__(self, source, label, **kwargs):
        super(BoxLayoutLevel, self).__init__(**kwargs)
        self.orientation = 'horizontal'  # Set layout orientation to horizontal
        self.padding = 20  # Set padding inside the layout
        self.spacing = 20  # Set spacing between elements

        # Add an image representing the obstacle or item
        self.add_widget(Image(source=source, size_hint_x=.2))

        # Add a label describing the obstacle or item
        self.add_widget(Label(
            text=label,
            font_size=20,
            font_name=constants.PIXEL_REGULAR,
            halign='left',
            valign='top',
            size_hint_x=.8,
            pos_hint={'x': 0},
            markup=True
        ))
