import os

class Config:

    # DB settings
    DB_URI = 'mongodb://localhost:27017'

    DBNAME = 'sensors-db'
    COLLECTION_NAME = 'sensors_data'

    # Map generation parameters
    STEEPNESS_MIN = 35
    STEEPNESS_MAX = 120
    SECTION_LENGTH_MIN = 25
    SECTION_LENGTH_MAX = 65
    SPACE_MIN = 11
    SPACE_MAX = 22
    OBSTACLES_TYPES = ['point', 'stalactite', 'junction', 'deadend']
    NARROW_OBSTACLES_TYPES = ['point', 'stalactite']

    TOP_WALL = 1
    TOP_WALL_BOTTOM = 2
    MIDDLE_WALL = 3
    BOTTOM_WALL_TOP = 4
    BOTTOM_WALL = 5
    WALLS = (
        TOP_WALL, TOP_WALL_BOTTOM, MIDDLE_WALL, BOTTOM_WALL_TOP, BOTTOM_WALL
    )
    SMALL_OBJECTS = (6, 7, 8, 9, 10, 11, 12, 13, 14)
    SMALL_OBJECT_CHANCE = 50
    FINISH = 15

    WALL = 39
    EMPTY = 0

    # keys
    LABEL_KEYS = ['u', 'l', 'r']


class ConfigDocker(Config):
    DB_URI = 'mongodb://db:27017'


config = ConfigDocker() if os.environ.get('DOCKER_ENVIRONMENT') == 'True' else Config()
