from random import choices
MOVE_DIR = ['left', 'right', 'up', 'down']
RANDOM_WALK_BUFFER = 40
TARGETING_BUFFER = 0


# determine next move using direction weighting
# positive x distance shows the distance to the right of the object
# positive y distance shows the distance below the element
def direction_weighting(x, y):
    weights = [fun(x, y, RANDOM_WALK_BUFFER)
               for fun in (left_prob, right_prob, up_prob, down_prob)]
    direction = choices(population=MOVE_DIR, weights=weights, k=1)[0]
    return direction


# determine the next move for an entity targeting a location (deterministic)
def move_direction_to_target(x, y):
    weights = [fun(x, y, TARGETING_BUFFER)
               for fun in (left_prob, right_prob, up_prob, down_prob)]
    direction = choices(population=MOVE_DIR, weights=weights, k=1)[0]
    return direction

##
# CRUDE WEIGHTING FUNCTION, MORE WORK LATER
##


def left_prob(x, y, buffer):
    return max(x, 0) + buffer


def right_prob(x, y, buffer):
    return max(-x, 0) + buffer


def up_prob(x, y, buffer):
    return max(y, 0) + buffer


def down_prob(x, y, buffer):
    return max(-y, 0) + buffer
