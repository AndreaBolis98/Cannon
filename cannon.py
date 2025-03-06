from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Rotate, PushMatrix, PopMatrix
from math import sqrt, sin, cos, pow, acos, degrees, radians
import copy
from projectile import Bullet, Bombshell, Laser
import constants

class Cannon(Image):
    
    def __init__(self, **kwargs):
        super(Cannon, self).__init__(**kwargs)
        # Maintain aspect ratio for the cannon
        pix_y = constants.SCREEN_HEIGHT * self.size_hint_y  # Calculate pixel height based on size hint
        pix_x = pix_y * 1.1  # Calculate width maintaining a 1.1 aspect ratio
        self.size_hint_x = (pix_x / constants.SCREEN_WIDTH)  # Adjust size_hint_x based on width
        self.reset()  # Reset the cannon's state (velocity, angle, etc.)
        self._draw()  # Initialize the graphics

    def _draw(self):  # Setup graphics, ensuring rotation is about the center of the cannon
        # Initialize cannon settings
        self.qty_muzzle = copy.copy(constants.INITAL_COUNTER)  # Copy initial muzzle counter values
        self.muzzle_type = 0  # Set initial muzzle type
        self.shooting = False  # Shooting flag, set to False initially

        # Setup the rotation matrix to rotate the cannon around its center
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()  # Create a Rotate object to handle rotation
            self.rot.origin = self.center  # Set the origin of rotation to the center of the widget
            self.rot.axis = (0, 0, 1)  # Set rotation axis (z-axis for 2D)
        with self.canvas.after:
            PopMatrix()

    def change_muzzle(self, index):  # Change the muzzle type based on the given index
        if not self.shooting:  # Ensure muzzle type can only be changed when not shooting
            if index > 2:  # Wrap around the muzzle type if index exceeds 2
                index = 0

            self.muzzle_type = index  # Update the muzzle type

            # Check if the selected muzzle type has any ammunition
            if self.qty_muzzle[self.muzzle_type] <= 0:
                self.change_muzzle(self.muzzle_type + 1)  # Switch to the next available muzzle

            # Handle visibility of the power cannon widget based on muzzle type
            if self.muzzle_type == 2:  # Laser type doesn't require power
                self.parent.remove_widget(self.parent.parent.parent.power_cannon)
            elif not self.parent.parent.parent.power_cannon.parent:
                self.parent.add_widget(self.parent.parent.parent.power_cannon)

            # Update the UI to reflect the selected muzzle
            for amm in self.parent.parent.parent.ammunition:
                amm.updateColor(self.muzzle_type)

    def updateCounterMuzzle(self):  # Update the ammunition count for the current muzzle
        if self.qty_muzzle[self.muzzle_type] > 0:
            self.qty_muzzle[self.muzzle_type] -= 1  # Decrease the ammunition count
        cnt = True  # Flag to track if all ammunition has been used

        # Update the UI with the current ammunition count
        for amm in self.parent.parent.parent.ammunition:
            amm.count = f'{self.qty_muzzle[amm.index]}'
            if amm.count != '0':  # If there's any ammunition left, set cnt to False
                cnt = False

        # If the current muzzle runs out of ammunition and there's more left, switch to the next available one
        if self.qty_muzzle[self.muzzle_type] <= 0 and cnt == False:
            self.change_muzzle(self.muzzle_type + 1)
        return cnt

    def update_angle(self, pos):  # Update the rotation angle based on the mouse/touch position
        if not self.shooting:  # Only update angle when not shooting
            x = pos[0] - self.x  # Calculate the x offset
            y = pos[1] - self.y  # Calculate the y offset
            vect = sqrt(pow(x, 2) + pow(y, 2))  # Compute the vector magnitude
            angle = degrees(acos(x / vect))  # Calculate the angle in degrees
            self.angle = angle  # Update the cannon's angle
            self.rot.angle = angle  # Set the rotation angle
            self.rot.origin = self.center  # Ensure the origin of rotation is the center

    def reset(self):  # Reset the cannon's parameters (angle, velocity)
        self.velocity = 0  # Reset velocity to 0
        self.angle = NumericProperty(0)  # Reset angle to 0 (using Kivy's NumericProperty)

    def inc_velocity(self, dt):  # Increment the velocity when the mouse is held down
        self.velocity += 1  # Increase velocity
        if self.velocity > 100:  # Reset if velocity exceeds 100
            self.velocity = 0
        # Update the power cannon UI with the current velocity value
        self.parent.parent.parent.power_cannon.set_value(self.velocity)
    
    def start_shot(self):  # Start shooting based on the current muzzle type
        pos = self.initPos()  # Calculate the initial position for the projectile
        # Create a projectile based on the selected muzzle type
        if self.muzzle_type == 0:
            muzzle = Bullet(angle=self.angle, velocity=self.velocity, pos=pos)
        elif self.muzzle_type == 1:
            muzzle = Bombshell(angle=self.angle, velocity=self.velocity, pos=pos)
        elif self.muzzle_type == 2:
            muzzle = Laser(size=[100, constants.LASER_SIZE], angle=self.angle, pos=pos)

        self.shooting = True  # Set shooting flag to True
        return muzzle  # Return the created projectile

    def initPos(self):  # Calculate the initial position for the muzzle when shooting
        x = self.pos[0] + self.size[0] * cos(radians(self.angle))  # X-coordinate based on angle
        y = self.pos[1] + self.size[1] * sin(radians(self.angle))  # Y-coordinate based on angle
        self.initialPos = x, y  # Store the initial position
        return self.initialPos  # Return the initial position
