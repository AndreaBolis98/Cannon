from obstacleRock import Rock
from obstacleMirror import Mirror
from obstaclePerpetio import Perpetio
from obstacleWarmHole import WarmHole
import constants

# Main setup function to configure each level
def setup_level(level):
    # Return the objects for the appropriate level based on the level number
    if level == 1:
        return level_one()
    elif level == 2:
        return level_two()
    elif level == 3:
        return level_three()
    elif level == 4:
        return level_four()
    elif level == 5:
        return level_five()

# Level 1 configuration
def level_one():
    objects = []  # Initialize an empty list for level objects
    
    # Create various obstacles for level 1
    perpetio1 = Perpetio(pos=(constants.SCREEN_WIDTH * 77 / 100, constants.SCREEN_HEIGHT * 0 / 100), source=constants.PATH_PERPETIO)
    rock1 = Rock(pos=(constants.SCREEN_WIDTH * 80 / 100, constants.SCREEN_HEIGHT * 10 / 100))
    rock2 = Rock(pos=(constants.SCREEN_WIDTH * 83 / 100, constants.SCREEN_HEIGHT * 18 / 100))
    perpetio2 = Perpetio(pos=(constants.SCREEN_WIDTH * 87 / 100, constants.SCREEN_HEIGHT * 26 / 100), source=constants.PATH_PERPETIO)
    perpetio3 = Perpetio(pos=(constants.SCREEN_WIDTH * 90 / 100, constants.SCREEN_HEIGHT * 33 / 100), source=constants.PATH_PERPETIO)
    
    # Append created objects to the list
    objects.append(perpetio1)
    objects.append(rock1)
    objects.append(rock2)
    objects.append(perpetio2)
    objects.append(perpetio3)
    
    return objects  # Return the list of objects for level 1

# Level 2 configuration
def level_two():
    objects = []  # Initialize an empty list for level objects
    
    # Create various obstacles for level 2
    perpetio1 = Perpetio(pos=(constants.SCREEN_WIDTH * 75 / 100, constants.SCREEN_HEIGHT * 10 / 100), source=constants.PATH_PERPETIO)
    rock1 = Rock(pos=(constants.SCREEN_WIDTH * 75 / 100, constants.SCREEN_HEIGHT * 18 / 100))
    rock2 = Rock(pos=(constants.SCREEN_WIDTH * 75 / 100, constants.SCREEN_HEIGHT * 26 / 100))
    mirror1 = Mirror(pos=(constants.SCREEN_WIDTH * 80 / 100, constants.SCREEN_HEIGHT * 3 / 100), size=(10, 100), angle=0)
    mirror2 = Mirror(pos=(constants.SCREEN_WIDTH * 45 / 100, constants.SCREEN_HEIGHT * 60 / 100), size=(10, 100), angle=90)
    
    # Append created objects to the list
    objects.append(perpetio1)
    objects.append(rock1)
    objects.append(rock2)
    objects.append(mirror1)
    objects.append(mirror2)
    
    return objects  # Return the list of objects for level 2

# Level 3 configuration
def level_three():
    objects = []  # Initialize an empty list for level objects
    
    # Create various obstacles for level 3
    perpetio1 = Perpetio(pos=(constants.SCREEN_WIDTH * 50 / 100, constants.SCREEN_HEIGHT * 40 / 100), source=constants.PATH_PERPETIO)
    rock1 = Rock(pos=(constants.SCREEN_WIDTH * 82 / 100, constants.SCREEN_HEIGHT * 24 / 100))
    rock2 = Rock(pos=(constants.SCREEN_WIDTH * 87 / 100, constants.SCREEN_HEIGHT * 24 / 100))
    rock3 = Rock(pos=(constants.SCREEN_WIDTH * 92 / 100, constants.SCREEN_HEIGHT * 24 / 100))
    mirror1 = Mirror(pos=(constants.SCREEN_WIDTH * 80 / 100, constants.SCREEN_HEIGHT * 3 / 100), size=(10, 100), angle=0)
    
    # Create additional obstacles and wormholes
    rock4 = Rock(pos=(constants.SCREEN_WIDTH * 20 / 100, constants.SCREEN_HEIGHT * 49 / 100))
    rock5 = Rock(pos=(constants.SCREEN_WIDTH * 24 / 100, constants.SCREEN_HEIGHT * 44 / 100))
    rock6 = Rock(pos=(constants.SCREEN_WIDTH * 28 / 100, constants.SCREEN_HEIGHT * 39 / 100))
    
    warmhole_in = WarmHole(pos=(constants.SCREEN_WIDTH * 30 / 100, constants.SCREEN_HEIGHT * 50 / 100), source=constants.PATH_WARMHOLE_IN, is_in=True, angle=0)
    warmhole_out = WarmHole(pos=(constants.SCREEN_WIDTH * 85 / 100, constants.SCREEN_HEIGHT * 60 / 100), source=constants.PATH_WARMHOLE_IN, is_in=False, angle=-90)
    warmhole_in.warmHole_out = warmhole_out  # Link wormholes together
    
    # Append created objects to the list
    objects.append(warmhole_in)
    objects.append(warmhole_out)
    objects.append(perpetio1)
    objects.append(rock1)
    objects.append(rock2)
    objects.append(rock3)
    objects.append(rock4)
    objects.append(rock5)
    objects.append(rock6)
    objects.append(mirror1)

    return objects  # Return the list of objects for level 3

# Level 4 configuration
def level_four():
    objects = []  # Initialize an empty list for level objects
    
    # Create various obstacles for level 4
    perpetio1 = Perpetio(pos=(constants.SCREEN_WIDTH * 20 / 100, constants.SCREEN_HEIGHT * 35 / 100), source=constants.PATH_PERPETIO)
    perpetio2 = Perpetio(pos=(constants.SCREEN_WIDTH * 19 / 100, constants.SCREEN_HEIGHT * 5 / 100), source=constants.PATH_PERPETIO)
    perpetio3 = Perpetio(pos=(constants.SCREEN_WIDTH * 30 / 100, constants.SCREEN_HEIGHT * 10 / 100), source=constants.PATH_PERPETIO)
    perpetio4 = Perpetio(pos=(constants.SCREEN_WIDTH * 55 / 100, constants.SCREEN_HEIGHT * 12 / 100), source=constants.PATH_PERPETIO)
    
    rock1 = Rock(pos=(constants.SCREEN_WIDTH * 22 / 100, constants.SCREEN_HEIGHT * 24 / 100))
    rock2 = Rock(pos=(constants.SCREEN_WIDTH * 32 / 100, constants.SCREEN_HEIGHT * 32 / 100))
    rock3 = Rock(pos=(constants.SCREEN_WIDTH * 80 / 100, constants.SCREEN_HEIGHT * 10 / 100))
    rock4 = Rock(pos=(constants.SCREEN_WIDTH * 83 / 100, constants.SCREEN_HEIGHT * 18 / 100))
    mirror1 = Mirror(pos=(constants.SCREEN_WIDTH * 45 / 100, constants.SCREEN_HEIGHT * 50 / 100), size=(10, 100), angle=90)
    
    # Append created objects to the list
    objects.append(perpetio1)
    objects.append(perpetio2)
    objects.append(perpetio3)
    objects.append(perpetio4)
    objects.append(rock1)
    objects.append(rock2)
    objects.append(rock3)
    objects.append(rock4)
    objects.append(mirror1)

    return objects  # Return the list of objects for level 4

# Level 5 configuration
def level_five():
    objects = []  # Initialize an empty list for level objects
    
    # Create various obstacles for level 5
    mirror1 = Mirror(pos=(constants.SCREEN_WIDTH * 75 / 100, constants.SCREEN_HEIGHT * 3 / 100), size=(10, 100), angle=0)
    mirror2 = Mirror(pos=(constants.SCREEN_WIDTH * 77 / 100, constants.SCREEN_HEIGHT * 17 / 100), size=(10, 100), angle=-30)
    mirror3 = Mirror(pos=(constants.SCREEN_WIDTH * 81 / 100, constants.SCREEN_HEIGHT * 26 / 100), size=(10, 100), angle=-45)
    mirror4 = Mirror(pos=(constants.SCREEN_WIDTH * 86 / 100, constants.SCREEN_HEIGHT * 30 / 100), size=(10, 100), angle=-90)
    
    rock1 = Rock(pos=(constants.SCREEN_WIDTH * 66 / 100, constants.SCREEN_HEIGHT * 59 / 100))
    rock2 = Rock(pos=(constants.SCREEN_WIDTH * 70 / 100, constants.SCREEN_HEIGHT * 54 / 100))
    rock3 = Rock(pos=(constants.SCREEN_WIDTH * 74 / 100, constants.SCREEN_HEIGHT * 49 / 100))
    rock4 = Rock(pos=(constants.SCREEN_WIDTH * 66 / 100, constants.SCREEN_HEIGHT * 66 / 100))
    rock5 = Rock(pos=(constants.SCREEN_WIDTH * 66 / 100, constants.SCREEN_HEIGHT * 72 / 100))
    
    warmhole_in = WarmHole(pos=(constants.SCREEN_WIDTH * 80 / 100, constants.SCREEN_HEIGHT * 60 / 100), source=constants.PATH_WARMHOLE_IN, is_in=True, angle=0)
    warmhole_out = WarmHole(pos=(constants.SCREEN_WIDTH * 79 / 100, constants.SCREEN_HEIGHT * 4 / 100), source=constants.PATH_WARMHOLE_IN, is_in=False, angle=0)
    warmhole_in.warmHole_out = warmhole_out  # Link wormholes together
    
    # Append created objects to the list
    objects.append(rock1)
    objects.append(rock2)
    objects.append(rock3)
    objects.append(rock4)
    objects.append(rock5)
    objects.append(warmhole_in)
    objects.append(warmhole_out)
    objects.append(mirror1)
    objects.append(mirror2)
    objects.append(mirror3)
    objects.append(mirror4)

    return objects  # Return the list of objects for level 5
