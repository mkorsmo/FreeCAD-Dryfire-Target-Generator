TARGET_WIDTH = 450.0
TARGET_HEIGHT = 570.0

DEFAULT_SCALE = 1 / 3
DEFAULT_THICKNESS = 1.2
DEFAULT_GROOVE_WIDTH = 0.6
DEFAULT_GROOVE_DEPTH = 0.3
DEFAULT_INCLUDE_PERIMETER = True

NON_SCORING_BORDER = 5.0


# Coordinates are centered on X and measured upward from the bottom
# of the target. Dimensions come from the IPSC target drawing supplied
# for this implementation.
TARGET_OUTLINE = [
    (-75.0, 0.0),
    (75.0, 0.0),
    (225.0, 190.0),
    (225.0, 380.0),
    (75.0, 570.0),
    (-75.0, 570.0),
    (-225.0, 380.0),
    (-225.0, 190.0),
]


# A-zone dimensions from the supplied drawing:
# top flat:       X = +/- 25 mm, Y = 545 mm
# upper shoulder: X = +/- 75 mm, Y = 380 mm
# lower shoulder: X = +/- 75 mm, Y = 295 mm
# bottom flat:    X = +/- 25 mm, Y = 220 mm
A_BOUNDARY = [
    (-25.0, 220.0),
    (25.0, 220.0),
    (75.0, 295.0),
    (75.0, 380.0),
    (25.0, 545.0),
    (-25.0, 545.0),
    (-75.0, 380.0),
    (-75.0, 295.0),
]


# The lower and side portions of the C/D boundary are explicitly
# dimensioned in the supplied drawing. The top two points coincide
# with the 5 mm non-scoring border and are calculated in target.py.
C_D_BOTTOM_LEFT = (-50.0, 120.0)
C_D_BOTTOM_RIGHT = (50.0, 120.0)

C_D_LOWER_LEFT = (-150.0, 235.0)
C_D_LOWER_RIGHT = (150.0, 235.0)

C_D_UPPER_LEFT = (-150.0, 380.0)
C_D_UPPER_RIGHT = (150.0, 380.0)
