INCH = 25.4

DEFAULT_SCALE = 1 / 3
DEFAULT_THICKNESS = 1.2


ROUND_PLATE_8 = 8.0 * INCH
ROUND_PLATE_10 = 10.0 * INCH
ROUND_PLATE_12 = 12.0 * INCH

SQUARE_PLATE_6 = 6.0 * INCH
SQUARE_PLATE_8 = 8.0 * INCH
SQUARE_PLATE_10 = 10.0 * INCH
SQUARE_PLATE_12 = 12.0 * INCH


# USPSA popper matched to the user's reference image.
USPSA_POPPER_TOTAL_HEIGHT = 42.0 * INCH
USPSA_POPPER_BODY_RADIUS = 6.0 * INCH
USPSA_POPPER_BODY_DIAMETER = 12.0 * INCH
USPSA_POPPER_BODY_CENTER_Y = 27.375 * INCH

USPSA_POPPER_HEAD_RADIUS = 3.0 * INCH
USPSA_POPPER_HEAD_WIDTH = 6.0 * INCH

USPSA_POPPER_STEM_BASE_WIDTH = 6.0 * INCH
USPSA_POPPER_STEM_JOIN_WIDTH = 8.0 * INCH


# Mini-popper matched to the user's metric reference image.
# - overall height: 560 mm
# - body radius: 100 mm
# - body center height: 460 mm
# - stem/body chord width: 135 mm
# - base width: 100 mm
USPSA_MINI_POPPER_TOTAL_HEIGHT = 560.0
USPSA_MINI_POPPER_BODY_RADIUS = 100.0
USPSA_MINI_POPPER_BODY_DIAMETER = 200.0
USPSA_MINI_POPPER_BODY_CENTER_Y = 460.0

USPSA_MINI_POPPER_STEM_BASE_WIDTH = 100.0
USPSA_MINI_POPPER_STEM_JOIN_WIDTH = 135.0


TARGET_TYPES = {
    "round_8": {
        "label": 'Round Plate - 8"',
        "kind": "round",
        "width": ROUND_PLATE_8,
        "height": ROUND_PLATE_8,
        "diameter": ROUND_PLATE_8,
    },
    "round_10": {
        "label": 'Round Plate - 10"',
        "kind": "round",
        "width": ROUND_PLATE_10,
        "height": ROUND_PLATE_10,
        "diameter": ROUND_PLATE_10,
    },
    "round_12": {
        "label": 'Round Plate - 12"',
        "kind": "round",
        "width": ROUND_PLATE_12,
        "height": ROUND_PLATE_12,
        "diameter": ROUND_PLATE_12,
    },
    "square_6": {
        "label": 'Square Plate - 6"',
        "kind": "square",
        "width": SQUARE_PLATE_6,
        "height": SQUARE_PLATE_6,
        "side": SQUARE_PLATE_6,
    },
    "square_8": {
        "label": 'Square Plate - 8"',
        "kind": "square",
        "width": SQUARE_PLATE_8,
        "height": SQUARE_PLATE_8,
        "side": SQUARE_PLATE_8,
    },
    "square_10": {
        "label": 'Square Plate - 10"',
        "kind": "square",
        "width": SQUARE_PLATE_10,
        "height": SQUARE_PLATE_10,
        "side": SQUARE_PLATE_10,
    },
    "square_12": {
        "label": 'Square Plate - 12"',
        "kind": "square",
        "width": SQUARE_PLATE_12,
        "height": SQUARE_PLATE_12,
        "side": SQUARE_PLATE_12,
    },
    "uspsa_popper": {
        "label": "USPSA Popper",
        "kind": "uspsa_popper",
        "width": USPSA_POPPER_BODY_DIAMETER,
        "height": USPSA_POPPER_TOTAL_HEIGHT,
    },
    "uspsa_mini_popper": {
        "label": "USPSA Mini-Popper",
        "kind": "uspsa_mini_popper",
        "width": USPSA_MINI_POPPER_BODY_DIAMETER,
        "height": USPSA_MINI_POPPER_TOTAL_HEIGHT,
    },
}
