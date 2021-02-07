from random import choices
MOVE_DIR = ['left', 'right', 'up', 'down']


# determine next move using direction weighting
# positive x distance shows the distance to the right of the object
# positive y distance shows the distance below the element
def direction_weighting(x, y):
    weights = [fun(x, y)
               for fun in (left_prob, right_prob, up_prob, down_prob)]
    direction = choices(population=MOVE_DIR, weights=weights, k=1)[0]
    return direction

##
# CRUDE WEIGHTING FUNCTION, MORE WORK LATER
##


def left_prob(x, y):
    return max(x, 0) + 40


def right_prob(x, y):
    return max(-x, 0) + 40


def up_prob(x, y):
    return max(y, 0) + 40


def down_prob(x, y):
    return max(-y, 0) + 40
