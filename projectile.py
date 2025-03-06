from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, Rotate, PushMatrix, PopMatrix
from kivy.properties import NumericProperty
from kivy.vector import Vector
from obstacleMirror import Mirror
from obstaclePerpetio import Perpetio
from obstacleRock import Rock
from obstacleWarmHole import WarmHole
import math
import constants

# BaseProjectile class handles common projectile behavior (e.g., velocity, angle, movement)
class BaseProjectile(Widget):
    velocity = NumericProperty(0)  # Speed of the projectile
    mass = NumericProperty(0)      # Mass for gravity effect
    time = NumericProperty(0)      # Time for calculating trajectory
    angle = NumericProperty(0)     # Angle of launch
    warnHoleAngle = 0              # Angle for wormhole exit

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialPos = Vector(*self.pos)  # Store initial position as a Vector
        self.update_velocity()  # Calculate initial velocity components
        self.inc = [0, 0]  # Used for wormhole position adjustments

    # Update velocity components based on angle and magnitude
    def update_velocity(self):
        coseno = math.cos(math.radians(self.angle))
        seno = math.sin(math.radians(self.angle))
        self.velx = self.velocity * coseno  # Horizontal velocity
        self.vely = self.velocity * seno    # Vertical velocity
        self.time = 0

    # Move the projectile and check for collisions
    def move(self):  
        stateCollision = self.check_collision(self.parent)  # Check if there's a collision
        if stateCollision > 0:
            return stateCollision

        # Calculate new position based on velocity and gravity
        x = self.velx * self.time
        y = self.vely * self.time - 0.5 * self.mass * pow(self.time, 2)

        # Update trajectory and position
        self.calcTangente(x, y, self.velx, self.vely, self.time, self.angle)
        self.pos = x + self.initialPos[0] + self.inc[0], y + self.initialPos[1] + self.inc[1]

        self.time += constants.FPS * 5  # Increment time
        # Check if projectile goes out of bounds
        if (self.x + self.size[0] > constants.SCREEN_WIDTH) or (self.y < 0):
            return 3
        return 0

    # Calculate tangent angle of the trajectory for visual rotation
    def calcTangente(self, oldx, oldy, velx, vely, time, _angle):
        tmpTime = time + 1
        x = velx * tmpTime
        y = vely * tmpTime - 0.5 * self.mass * pow(tmpTime, 2)
        vectx = x - oldx
        vecty = y - oldy
        vect = math.sqrt(pow(vecty, 2) + pow(vectx, 2))
        angle = math.degrees(math.acos(vectx / vect))

        # Rotate projectile based on the tangent of the trajectory
        if vecty >= 0:
            self.rot.angle = angle - 90
        else:
            self.rot.angle = -angle - 90
        self.rot.origin = self.center

    # Check for collision with various objects
    def check_collision(self, root):
        if self.collide_widget(root.target):
            return 1  # Collision with the target

        # Iterate over objects in the environment and check for collisions
        for obj in root.objects:
            if self.collide_widget(obj):
                if isinstance(obj, Rock):
                    for part in obj.parts[:]:  
                        if self.collide_widget(part):
                            return self.manage_collision_rock(obj, part) # Handle part rock collision
                elif isinstance(obj, Mirror):
                    return self.manage_collision_mirror(obj)  # Handle mirror collision
                elif isinstance(obj, Perpetio):
                    return self.manage_collision_perpetio()  # Handle Perpetio collision
                elif isinstance(obj, WarmHole):
                    if obj.is_in:
                        return self.manage_collision_wormhole(obj)  # Handle wormhole entry

        return 0  # No collision

    # Manage wormhole collision (teleport the projectile)
    def manage_collision_wormhole(self, elem):
        shift_x = elem.warmHole_out.center_x - self.initialPos[0]  # Shift to wormhole exit
        shift_y = elem.warmHole_out.center_y - self.initialPos[1]
        self.inc = [shift_x, shift_y]
        self.angle = elem.warmHole_out.angle  # Update angle for new trajectory
        self.update_velocity()  # Recalculate velocity components
        return 0

# Projectile class extending the BaseProjectile and Image class
class Projectile(BaseProjectile, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set size and fit based on provided size hints
        if 'size_hint' in kwargs:
            self.size_hint = kwargs['size_hint']
        if self.size_hint_y is not None:
            pix_y = constants.SCREEN_HEIGHT * self.size_hint_y
            pix_x = pix_y * 0.7
            self.size_hint_x = pix_x / constants.SCREEN_WIDTH

        self.time = 0
        self.fit_mode = 'fill'

        # Handle rotation of the projectile
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle = self.angle - 90
            self.rot.origin = self.center
        with self.canvas.after:
            PopMatrix()

        self.bind(pos=self.update_rotation, size=self.update_rotation)

    # Update the rotation origin based on the current center
    def update_rotation(self, *args):
        self.rot.origin = self.center

    # Handle collision with rock and remove affected parts
    def manage_collision_rock(self, elem,part):
        hit = 0
        for part in elem.parts[:]:  # Loop through the rock parts
            if self.is_within_radius(part.center, self.center, self.radius, 5):
                elem.parts.remove(part)  # Remove part if within radius
                elem.remove_widget(part)
                hit = 2

        if len(elem.parts) <= 0:  # Remove the entire rock if no parts are left
            self.parent.remove_widget(elem)
            self.parent.objects.remove(elem)
        return hit

    # Check if part of the rock is within a given radius
    def is_within_radius(self, point, center, radius, penetration):
        dist = Vector(point).distance(Vector(center)) - penetration
        return dist <= radius

    # Handle collision with mirror
    def manage_collision_mirror(self, elem):
        self.parent.remove_widget(self)
        return 2

    # Handle collision with Perpetio
    def manage_collision_perpetio(self):
        self.parent.remove_widget(self)
        return 2

# Bullet class representing a specific type of projectile
class Bullet(Projectile):
    radius = constants.BULLET_RADIUS
    drill = constants.BULLET_DRILL
    mass = constants.BULLET_MASS

    def __init__(self, angle, velocity, pos, **kwargs):
        super().__init__(source=constants.PATH_BULLET, angle=angle, velocity=velocity, size_hint=constants.BULLET_SIZE, pos=pos, **kwargs)

# Bombshell class representing another type of projectile
class Bombshell(Projectile):
    radius = constants.BOMB_RADIUS
    drill = constants.BOMB_DRILL
    mass = constants.BOMB_MASS

    def __init__(self, angle, velocity, pos, **kwargs):
        super().__init__(source=constants.PATH_BOMB, angle=angle, velocity=velocity, size_hint=constants.BOMB_SIZE, pos=pos, **kwargs)

# LaserSegment class that handles laser behavior
class LaserSegment(BaseProjectile):
    mirrorCollision = None
    drill = 0
    radius = constants.LASER_RADIUS

    def __init__(self, heightParent, vector, **kwargs):
        super(LaserSegment, self).__init__(**kwargs)
        self.vector = vector
        self.size = [heightParent, heightParent]
        self.radius = self.size[0] * 3
        self.velocity = constants.LASER_VEL
        self.initialPos = Vector(*self.pos)
        self.size_hint = (None, None)

        with self.canvas:
            PushMatrix()
            Color(1, 0, 0)  # Set the laser color to red
            self.rect = Rectangle(pos=self.pos, size=self.size)
            PopMatrix()

    # Reflect the laser when it hits a mirror
    def reflect(self, mirror_angle):
        angleLaser = math.atan(self.vector.y / self.vector.x)
        angleLaserdeg = math.degrees(angleLaser)
        incidence_angle = math.radians(mirror_angle + (mirror_angle - angleLaserdeg))
        reflection = Vector(self.vector.x * math.cos(incidence_angle), self.vector.y * math.sin(incidence_angle))
        self.vector = reflection

    # Move the laser segment and check for collisions
    def move(self):
        self.pos = Vector(*self.pos) + self.vector + self.inc
        self.inc = [0, 0]
        self.rect.pos = self.pos
        return self.check_collision(self.parent.parent)

    # Manage collision with rock (remove part)
    def manage_collision_rock(self, elem, part):
        elem.remove_widget(part)
        elem.parts.remove(part)
        return 2

    # Handle mirror collision (reflect)
    def manage_collision_mirror(self, elem):
        if self.collide_widget(elem) and self.mirrorCollision != elem:
            self.mirrorCollision = elem
            self.reflect(elem.angle - 90)
        return 0

    # Handle Perpetio collision
    def manage_collision_perpetio(self):
        self.parent.parent.remove_widget(self)
        return 2

    # Handle wormhole collision (teleport laser)
    def manage_collision_wormhole(self, elem):
        shift_x = elem.warmHole_out.center_x - self.x
        shift_y = elem.warmHole_out.center_y - self.y
        self.inc = [shift_x, shift_y]
        self.vector = Vector(self.vector.x * math.cos(math.radians(elem.warmHole_out.angle)), self.vector.y * math.sin(math.radians(elem.warmHole_out.angle)))
        return 0

# Laser class for handling a series of laser segments
class Laser(Widget):
    num_elem = 0
    angle = 0

    def __init__(self, angle, pos, **kwargs):
        super(Laser, self).__init__(pos=pos, **kwargs)
        self.angle = math.radians(angle)
        self.size_hint = (None, None)
        self.segments = []
        self.vector = Vector(constants.LASER_VEL * math.cos(self.angle), constants.LASER_VEL * math.sin(self.angle))

    # Move the laser and create new segments as it travels
    def move(self):
        if self.num_elem < constants.LASER_LENGTH:
            self.num_elem += 1
            self.create_segment(self.pos)

        for segment in self.segments:
            state_collision = segment.move()

        if state_collision == 2:
            self.remove_widget(self.segments.pop())
        elif state_collision == 1:
            return 1

        if len(self.segments) == 0:
            return 2

        if (self.segments[0].x + self.segments[0].size[0] > constants.SCREEN_WIDTH) or (self.segments[0].x < 0) or (self.segments[0].y < 0) or (self.segments[0].y + self.segments[0].size[1] > constants.SCREEN_HEIGHT):
            return 3
        return 0

    # Create and add a new segment to the laser
    def create_segment(self, pos):
        segment = LaserSegment(pos=pos, heightParent=self.height, vector=self.vector)
        self.segments.insert(0, segment)
        self.add_widget(segment)
