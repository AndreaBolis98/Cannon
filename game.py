from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from endGame import TransparentOverlay
from cannon import Cannon
from target import Target
from kivy.core.window import Window
from kivy.clock import Clock
from customWidget.Card.card_ammunition import CardAmmunition
from customWidget.Card.record import RecordCard
from obstacleRock import Rock
from progressBar import CustomProgressBar
from customFloatLayout import CustomFloatLayout
from projectile import Laser
from customWidget.Card.home_btn import IconButton
import copy
import constants
import level
import saveResult

class GamePage(Screen):
    qty_muzzle = []  # A list to track the available ammunition for different types of projectiles (bullet, bomb, laser)

    def __init__(self, **kw):
        super().__init__(**kw)  # Initialize the screen using the Screen class constructor

    # This method is called when the screen is entered
    def on_enter(self):
        super().on_enter()  # Call the parent class method
        self.clear_widgets()  # Clear any existing widgets on the screen
        Window.bind(mouse_pos=self.mouse_pos)  # Bind mouse position to update cannon angle
        self.points = copy.copy(constants.INITIAL_POINT)  # Set initial points
        self.level = 0  # Set initial game level
        self.gameFinish = False  # Set flag to indicate the game has not finished
        self.qty_muzzle = copy.copy(constants.INITAL_COUNTER)  # Copy the initial ammunition count
        self.objects = []  # Initialize the list for obstacles and objects

        self.initializationaPage()  # Set up the game page layout and elements
        Clock.schedule_once(self.updateLevel, 0.1)  # Schedule the first level update after a brief delay

    # This method is called when leaving the screen
    def on_leave(self):
        super().on_leave()  # Call the parent class method

    # MOUSE ACTIONS

    # This method is called when the mouse moves, updating the cannon's angle
    def mouse_pos(self, window, pos):
        if not self.gameFinish:  # Only update if the game is not finished
            self.cannon.update_angle(pos)  # Update cannon visualization based on mouse position

    # Called when the mouse button is held down, starts increasing cannon velocity
    def touch_down(self):
        if not self.cannon.shooting and not self.gameFinish:  # Check if the cannon is not shooting and game is active
            self.scheduleVel = Clock.schedule_interval(self.cannon.inc_velocity, constants.FPS_SET_VELOCITY)  # Increment velocity

    # Called when the mouse button is released, fires the projectile
    def on_touch_up(self, touch):
        if not self.cannon.shooting and hasattr(self, "scheduleVel"):  # Check if shooting is allowed and velocity scheduling exists
            self.scheduleVel.cancel()  # Stop increasing velocity
            del self.scheduleVel  # Delete the schedule
            self.projectile = self.cannon.start_shot()  # Start the shot and return the projectile instance
            self.add_widget(self.projectile)  # Add the projectile widget to the screen
            self.points -= constants.AMMU_POINTS[self.cannon.muzzle_type]  # Deduct points based on the type of ammunition
            self.updatePoint(self.points)  # Update the points display
            self.scheduleShot = Clock.schedule_interval(self.shot, constants.FPS)  # Schedule the projectile movement

    # SHOT MANAGEMENT

    # This method moves the projectile each frame and checks its state
    def shot(self, dt):
        state = self.projectile.move()  # Move the projectile and check its state (1 for hit, >0 for other collisions)
        if state > 0:
            self.endShot(state)  # If the shot ends, handle post-shot behavior

    # This method handles the end of the shot, including cleanup and checking for hits
    def endShot(self, state):
        self.scheduleShot.cancel()  # Stop updating the projectile's position
        self.power_cannon.value = 0  # Reset the power bar
        self.cannon.velocity = 0  # Reset the cannon's velocity
        self.remove_widget(self.projectile)  # Remove the projectile from the screen
        self.cannon.shooting = False  # Set shooting flag to False

        if self.cannon.updateCounterMuzzle():  # Check if the ammunition runs out
            self.endGame(False)  # End the game if no ammo is left

        # If the projectile is not a laser and has hit something, display an explosion effect
        if state > 0 and self.projectile is not Laser:
            self.explosion = Image(source=constants.PATH_EXPLOSION, pos=self.projectile.pos, size_hint=constants.EXPLOSION_SIZE)
            self.add_widget(self.explosion)
            Clock.schedule_interval(self.remove_explosion, 2)  # Remove the explosion after 2 seconds

        if state == 1:
            self.target.is_hit()  # If the target is hit, handle the target's hit logic

    # Remove the explosion effect after a set time
    def remove_explosion(self, dt):
        self.remove_widget(self.explosion)  # Remove the explosion widget from the screen
        Clock.unschedule(self.remove_explosion)  # Stop the scheduled explosion removal

    # LEVEL METHODS

    # Update the level by incrementing the level, points, and setting up new obstacles
    def updateLevel(self, dt):
        if self.level == constants.MAX_LEVEL:  # If the max level is reached, end the game
            self.endGame(True)
            return

        self.level += 1  # Increment the level
        self.points += 2000  # Add 2000 points for advancing to the next level
        self.writeLevel(self.level)  # Update the level display
        self.updatePoint(self.points)  # Update the points display

        self.target.pos_hint = constants.TARGET_POS  # Set the target's position
        self.setup_level()  # Set up the objects and obstacles for the new level

    # Setup the objects and obstacles for the current level
    def setup_level(self):
        self.clearObject()  # Clear previous level's objects
        self.objects = level.setup_level(self.level)  # Get the new objects for the current level
        for obj in self.objects:
            self.layoutGame.add_widget(obj)  # Add each object to the game layout

    # Clear the objects from the previous level
    def clearObject(self):
        for obj in self.objects:
            self.layoutGame.remove_widget(obj)  # Remove each object from the layout
        self.objects = []  # Reset the object list

    # Update the level display
    def writeLevel(self, level):
        self.level_wgt.text = f'[color=ffffff]LEVEL:[/color] [color=00ff00]{level}[/color]'

    # Update the points display, if points drop below 0, end the game
    def updatePoint(self, points):
        if points >= 0:
            self.points_wgt.text = f'[color=ffffff]HI:[/color] [color=00ff00]{points}[/color]'
        else:
            self.points_wgt.text = f'[color=ffffff]HI:[/color] [color=ff0000]0[/color]'
            self.endGame(False)  # End the game if points drop below 0

    # GAME ENDING

    # End the game and display the appropriate overlay based on win/loss
    def endGame(self, win):
        self.gameFinish = True  # Set the game finish flag to True
        self.overlayEndGame = TransparentOverlay(
            pos=self.layoutGame.pos,
            size=self.layoutGame.size,
            level=self.level,
            points=self.points,
            count=self.qty_muzzle,
            win=win
        )
        self.layoutGame.add_widget(self.overlayEndGame)  # Add the endgame overlay to the layout

        if win:
            Clock.schedule_interval(self.update_points, 0.5)  # If won, continue updating points
        else:
            self.overlayEndGame.get_classification()  # Get the player's classification if the game is lost
            self.overlayEndGame.add_exit()  # Add an exit button

    # Continuously update the points during the game and check if all ammunition is used
    def update_points(self, dt):
        if self.qty_muzzle[self.cannon.muzzle_type] > 0:
            self.overlayEndGame.update_points(constants.AMMU_POINTS[self.cannon.muzzle_type])  # Update points for remaining ammunition

        if self.cannon.updateCounterMuzzle():
            Clock.unschedule(self.update_points)  # Stop updating points if no ammunition is left
            self.overlayEndGame.add_exit()  # Add an exit button when finished

    # HANDLE BUTTONS

    # Home button press handling
    def homebtn(self, page):
        self.show_popup()  # Show a confirmation popup when pressing the home button

    # Show a popup to confirm exiting the game
    def show_popup(self):
        # Create the content for the popup
        popup_content = BoxLayout(orientation='vertical')
        popup_label = Label(text="IF YOU CONFIRM THE SCORE WILL BE LOST", font_size=27, font_name=constants.PIXEL_REGULAR)
        popup_buttons = BoxLayout(orientation='horizontal')
        
        # Create cancel and confirm buttons
        btn_confirm_popup = Button(text="Cancel", background_color=[0, 1, 0, 1], font_size=25, font_name=constants.PIXEL_REGULAR)
        btn_confirm_popup.bind(on_release=self.close_popup)
        
        btn_close_popup = Button(text="Confirm", background_color=[1, 0, 0, 1], font_size=25, font_name=constants.PIXEL_REGULAR)
        btn_close_popup.bind(on_release=self.confirm)

        # Add label and buttons to the popup content
        popup_content.add_widget(popup_label)
        popup_content.add_widget(popup_buttons)
        popup_buttons.add_widget(btn_close_popup)
        popup_buttons.add_widget(btn_confirm_popup)

        # Create the popup itself
        self.popup = Popup(title="Exit", content=popup_content, size_hint=(None, None), size=(600, 200))
        self.popup.open()  # Open the popup

    # Close the popup
    def close_popup(self, instance):
        self.popup.dismiss()  # Dismiss the popup

    # Confirm exit and navigate to the home screen
    def confirm(self, instance):
        self.parent.current = 'home'  # Navigate to the home page
        self.popup.dismiss()  # Close the popup

    # PAGE OBJECT INITIALIZATION

    # Set up the initial layout of the game page
    def initializationaPage(self):
        score = saveResult.redFirstThree()  # Get the top scores for the records section
        backImage = Image(source=constants.PATH_BACK, fit_mode='fill')  # Background image for the game

        # Set up various layouts and widgets
        self.gridLayout = BoxLayout(orientation='vertical')
        self.header = BoxLayout(orientation='horizontal', pos_hint={"x": 0, "top": 1}, size_hint=(1, 0.25), padding=([20, 20, 20, 20]))
        
        # Create home button
        iconbtn = IconButton(constants.PATH_HOME, 'home', pos_hint={'x': 0, 'top': 1})

        self.levelInfo = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.bulletInfo = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=20)
        self.records = BoxLayout(orientation='horizontal', size_hint=(1, 1))

        # Labels for level and points
        self.level_wgt = Label(markup=True, font_size=30, font_name=constants.PIXEL_REGULAR)
        self.points_wgt = Label(markup=True, halign='left', font_size=30, font_name=constants.PIXEL_REGULAR)

        # Create ammunition cards for bullets, bombs, and lasers
        self.bullet_card = CardAmmunition(image_path=constants.PATH_BULLET, title='BULLET', count=f'{self.qty_muzzle[0]}', size_hint=(0.08, 1), index=0)
        self.bomb_card = CardAmmunition(image_path=constants.PATH_BOMB, title='BOMB', count=f'{self.qty_muzzle[1]}', size_hint=(0.08, 1), index=1)
        self.laser_card = CardAmmunition(image_path=constants.PATH_LASER, title='LASER', count=f'{self.qty_muzzle[2]}', size_hint=(0.08, 1), index=2)
        self.ammunition = [self.bullet_card, self.bomb_card, self.laser_card]  # Store the ammunition cards in a list

        # Create record cards for top 3 scores
        self.first = RecordCard(image_path=constants.PATH_STAR_GOLD, title=f'{score[0]}', size_hint=(1, 1))
        self.second = RecordCard(image_path=constants.PATH_STAR_SILVER, title=f'{score[1]}', size_hint=(1, 1))
        self.third = RecordCard(image_path=constants.PATH_STAR_BRONZE, title=f'{score[2]}', size_hint=(1, 1))

        # Create the cannon instance
        self.cannon = Cannon(source=constants.PATH_CANNON, size_hint_y=constants.CANNON_SIZE[1], pos_hint=constants.CANNON_POS, keep_ratio=True)

        # Set up the game layout and add widgets
        self.layoutGame = CustomFloatLayout(size_hint=(1, .75))
        self.power_cannon = CustomProgressBar(size_hint=constants.CANNON_POWER_SIZE, pos_hint=constants.CANNON_POWER_POS)
        self.target = Target(source=constants.PATH_TARGET, size_hint_y=constants.TARGET_SIZE[1], pos_hint=constants.TARGET_POS, keep_ratio=True)

        self.add_widget(backImage)  # Add the background image to the screen
        self.add_widget(self.gridLayout)  # Add the main grid layout

        # Set up the header section with level, ammunition, and records
        self.gridLayout.add_widget(self.header)
        self.header.add_widget(iconbtn)  # Add home button
        self.header.add_widget(self.levelInfo)
        self.levelInfo.add_widget(self.level_wgt)  # Add level label
        self.levelInfo.add_widget(self.points_wgt)  # Add points label

        self.header.add_widget(self.bulletInfo)
        self.bulletInfo.add_widget(self.bullet_card)  # Add bullet card
        self.bulletInfo.add_widget(self.bomb_card)  # Add bomb card
        self.bulletInfo.add_widget(self.laser_card)  # Add laser card

        self.header.add_widget(self.records)
        self.records.add_widget(self.second)  # Add second place record card
        self.records.add_widget(self.first)  # Add first place record card
        self.records.add_widget(self.third)  # Add third place record card

        # Add the game layout (cannon, target, etc.) to the grid layout
        self.gridLayout.add_widget(self.layoutGame)
        self.layoutGame.add_widget(self.cannon)  # Add cannon to game layout
        self.layoutGame.add_widget(self.power_cannon)  # Add power cannon bar
        self.layoutGame.add_widget(self.target)  # Add target widget
