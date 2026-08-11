import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.dialog import TargetSettingsDialog
from freecad_dryfire_target.geometry import (
    make_centered_rectangle,
    make_extruded_polygon,
    make_polyline_groove,
    make_rectangle_groove,
)


TARGET_WIDTH = 450.0
TARGET_HEIGHT = 750.0

DEFAULT_SCALE = 1 / 3
DEFAULT_THICKNESS = 1.2
DEFAULT_GROOVE_WIDTH = 0.6
DEFAULT_GROOVE_DEPTH = 0.3

DEFAULT_FACE_LAYER_THICKNESS = 0.4
DEFAULT_CENTER_STRIPE_WIDTH = 50.8

DEFAULT_DIAGONAL_SHOULDER_X = 150.0
DEFAULT_DIAGONAL_BOTTOM_X = 150.0
DEFAULT_TUXEDO_CENTER_WIDTH = 150.0
DEFAULT_TUXEDO_BODY_TOP = 600.0
DEFAULT_BODY_HARD_COVER_TOP = 600.0
DEFAULT_LOWER_HALF_HARD_COVER_TOP = 475.0


TARGET_OUTLINE = [
    (-150.0, 0.0),
    (150.0, 0.0),
    (225.0, 150.0),
    (225.0, 550.0),
    (150.0, 600.0),
    (75.0, 600.0),
    (75.0, 750.0),
    (-75.0, 750.0),
    (-75.0, 600.0),
    (-150.0, 600.0),
    (-225.0, 550.0),
    (-225.0, 150.0),
]


C_D_BOUNDARY = [
    (-75.0, 600.0),
    (-150.0, 550.0),
    (-150.0, 270.0),
    (-100.0, 150.0),
    (100.0, 150.0),
    (150.0, 270.0),
    (150.0, 550.0),
    (75.0, 600.0),
]


def make_target_outline(
    scale,
    thickness,
):
    return make_extruded_polygon(
        TARGET_OUTLINE,
        scale,
        thickness,
    )


def make_scored_target_shape(
    scale,
    thickness,
    groove_width,
    groove_depth,
):
    target_shape = make_extruded_polygon(
        TARGET_OUTLINE,
        scale,
        thickness,
    )

    upper_a_zone = make_rectangle_groove(
        100.0,
        50.0,
        675.0,
        scale,
        thickness,
        groove_width,
        groove_depth,
    )

    lower_a_zone = make_rectangle_groove(
        150.0,
        280.0,
        270.0,
        scale,
        thickness,
        groove_width,
        groove_depth,
    )

    c_d_boundary = make_polyline_groove(
        C_D_BOUNDARY,
        scale,
        thickness,
        groove_width,
        groove_depth,
    )

    target_shape = target_shape.cut(upper_a_zone)
    target_shape = target_shape.cut(lower_a_zone)
    target_shape = target_shape.cut(c_d_boundary)

    return target_shape


def add_scoring_grooves(
    target_shape,
    scale,
    thickness,
    groove_width,
    groove_depth,
    face="top",
):
    upper_a_zone = make_rectangle_groove(
        100.0,
        50.0,
        675.0,
        scale,
        thickness,
        groove_width,
        groove_depth,
        face=face,
    )

    lower_a_zone = make_rectangle_groove(
        150.0,
        280.0,
        270.0,
        scale,
        thickness,
        groove_width,
        groove_depth,
        face=face,
    )

    c_d_boundary = make_polyline_groove(
        C_D_BOUNDARY,
        scale,
        thickness,
        groove_width,
        groove_depth,
        face=face,
    )

    target_shape = target_shape.cut(upper_a_zone)
    target_shape = target_shape.cut(lower_a_zone)
    target_shape = target_shape.cut(c_d_boundary)

    return target_shape


def make_diagonal_left_mask(
    scale,
    thickness,
    shoulder_x=DEFAULT_DIAGONAL_SHOULDER_X,
    bottom_x=DEFAULT_DIAGONAL_BOTTOM_X,
):
    """
    USPSA Hardcover Version 3.

    Hard cover occupies the left side of the finished target.
    The diagonal runs from the upper-left shoulder to the
    lower-right edge of the target body.
    """
    points = [
        (-400.0, 850.0),
        (-shoulder_x, 600.0),
        (bottom_x, 0.0),
        (-400.0, -100.0),
    ]

    return make_extruded_polygon(
        points,
        scale,
        thickness,
    )


def make_diagonal_right_mask(
    scale,
    thickness,
    shoulder_x=DEFAULT_DIAGONAL_SHOULDER_X,
    bottom_x=DEFAULT_DIAGONAL_BOTTOM_X,
):
    """
    USPSA Hardcover Version 2.

    Hard cover occupies the right side of the finished target.
    The diagonal runs from the upper-right shoulder to the
    lower-left edge of the target body.
    """
    points = [
        (400.0, 850.0),
        (400.0, -100.0),
        (-bottom_x, 0.0),
        (shoulder_x, 600.0),
    ]

    return make_extruded_polygon(
        points,
        scale,
        thickness,
    )


def make_tuxedo_mask(
    scale,
    thickness,
    center_width=DEFAULT_TUXEDO_CENTER_WIDTH,
    body_top=DEFAULT_TUXEDO_BODY_TOP,
):
    """
    USPSA Hardcover Version 4, commonly called the Tuxedo target.

    Hard cover occupies both sides of the target body while
    leaving a centered scoring strip exposed. The head remains
    uncovered.
    """
    half_center_width = center_width / 2

    left_points = [
        (-400.0, -100.0),
        (-half_center_width, -100.0),
        (-half_center_width, body_top),
        (-400.0, body_top),
    ]

    right_points = [
        (half_center_width, -100.0),
        (400.0, -100.0),
        (400.0, body_top),
        (half_center_width, body_top),
    ]

    left_mask = make_extruded_polygon(
        left_points,
        scale,
        thickness,
    )

    right_mask = make_extruded_polygon(
        right_points,
        scale,
        thickness,
    )

    return left_mask.fuse(right_mask)


def make_right_half_mask(
    scale,
    thickness,
    center_width=DEFAULT_TUXEDO_CENTER_WIDTH,
    body_top=DEFAULT_TUXEDO_BODY_TOP,
):
    """
    USPSA Hardcover Version 6.

    This is the RIGHT-side half of the Tuxedo hard-cover pattern.
    The finished target keeps the same 150 mm-wide exposed center
    area as the Tuxedo target, with hard cover only on the right.
    """
    half_center_width = center_width / 2

    # build_hard_cover_target() rotates the finished geometry 180
    # degrees, so the pre-rotation mask is placed on the left side.
    points = [
        (-400.0, -100.0),
        (-half_center_width, -100.0),
        (-half_center_width, body_top),
        (-400.0, body_top),
    ]

    return make_extruded_polygon(
        points,
        scale,
        thickness,
    )


def make_left_half_mask(
    scale,
    thickness,
    center_width=DEFAULT_TUXEDO_CENTER_WIDTH,
    body_top=DEFAULT_TUXEDO_BODY_TOP,
):
    """
    USPSA Hardcover Version 7.

    This is the LEFT-side half of the Tuxedo hard-cover pattern.
    The finished target keeps the same 150 mm-wide exposed center
    area as the Tuxedo target, with hard cover only on the left.
    """
    half_center_width = center_width / 2

    # build_hard_cover_target() rotates the finished geometry 180
    # degrees, so the pre-rotation mask is placed on the right side.
    points = [
        (half_center_width, -100.0),
        (400.0, -100.0),
        (400.0, body_top),
        (half_center_width, body_top),
    ]

    return make_extruded_polygon(
        points,
        scale,
        thickness,
    )


def make_body_hard_cover_mask(
    scale,
    thickness,
    body_top=DEFAULT_BODY_HARD_COVER_TOP,
):
    """
    USPSA Hardcover Version 1.

    Hard cover occupies the entire main body of the target.
    The head remains uncovered.
    """
    points = [
        (-400.0, -100.0),
        (400.0, -100.0),
        (400.0, body_top),
        (-400.0, body_top),
    ]

    return make_extruded_polygon(
        points,
        scale,
        thickness,
    )


def make_lower_half_hard_cover_mask(
    scale,
    thickness,
    cover_top=DEFAULT_LOWER_HALF_HARD_COVER_TOP,
):
    """
    USPSA Hardcover Version 5.

    Hard cover occupies the lower half of the full 750 mm target,
    ending at 375 mm from the bottom.
    """
    points = [
        (-400.0, -100.0),
        (400.0, -100.0),
        (400.0, cover_top),
        (-400.0, cover_top),
    ]

    return make_extruded_polygon(
        points,
        scale,
        thickness,
    )


def build_hard_cover_target(
    document_name,
    scale,
    thickness,
    groove_width,
    groove_depth,
    hard_cover_mask,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    document = App.newDocument(document_name)

    if thickness <= 0.4:
        face_layer_thickness = thickness / 2
    else:
        face_layer_thickness = min(
            face_layer_thickness,
            thickness - 0.2,
        )

    back_thickness = thickness - face_layer_thickness

    back_shape = make_extruded_polygon(
        TARGET_OUTLINE,
        scale,
        back_thickness,
        z_offset=face_layer_thickness,
    )

    face_layer = make_extruded_polygon(
        TARGET_OUTLINE,
        scale,
        face_layer_thickness,
    )

    hard_cover_face = face_layer.common(hard_cover_mask)
    cardboard_face = face_layer.cut(hard_cover_face)

    effective_groove_depth = min(
        groove_depth,
        face_layer_thickness - 0.05,
    )

    cardboard_face = add_scoring_grooves(
        cardboard_face,
        scale,
        face_layer_thickness,
        groove_width,
        effective_groove_depth,
        face="bottom",
    )

    rotation_center = App.Vector(0, 0, 0)
    rotation_axis = App.Vector(0, 0, 1)

    back_shape.rotate(
        rotation_center,
        rotation_axis,
        180,
    )

    cardboard_face.rotate(
        rotation_center,
        rotation_axis,
        180,
    )

    hard_cover_face.rotate(
        rotation_center,
        rotation_axis,
        180,
    )

    back = document.addObject(
        "Part::Feature",
        "USPSA_Back",
    )
    back.Label = "USPSA Back"
    back.Shape = back_shape
    back.ViewObject.ShapeColor = (0.76, 0.56, 0.32)

    cardboard = document.addObject(
        "Part::Feature",
        "USPSA_Cardboard_Face",
    )
    cardboard.Label = "USPSA Cardboard Face"
    cardboard.Shape = cardboard_face
    cardboard.ViewObject.ShapeColor = (0.76, 0.56, 0.32)

    hard_cover = document.addObject(
        "Part::Feature",
        "USPSA_HardCover_Face",
    )
    hard_cover.Label = "USPSA Hard Cover Face"
    hard_cover.Shape = hard_cover_face
    hard_cover.ViewObject.ShapeColor = (0.1, 0.1, 0.1)

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewBottom()
    view.fitAll()

    return back, cardboard, hard_cover


def create_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
):
    document = App.newDocument("USPSA_DryFire_Target")

    target_shape = make_scored_target_shape(
        scale,
        thickness,
        groove_width,
        groove_depth,
    )

    target = document.addObject(
        "Part::Feature",
        "USPSA_Target",
    )

    target.Label = "USPSA Cardboard Target"
    target.Shape = target_shape
    target.ViewObject.ShapeColor = (0.76, 0.56, 0.32)

    document.recompute()

    Gui.activeDocument().activeView().viewTop()
    Gui.activeDocument().activeView().fitAll()

    return target


def create_body_hard_cover_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    body_mask = make_body_hard_cover_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="USPSA_Body_Hard_Cover_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=body_mask,
        face_layer_thickness=face_layer_thickness,
    )


def create_lower_half_hard_cover_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    lower_half_mask = make_lower_half_hard_cover_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="USPSA_Lower_Half_Hard_Cover_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=lower_half_mask,
        face_layer_thickness=face_layer_thickness,
    )


def create_center_stripe_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    stripe_width=DEFAULT_CENTER_STRIPE_WIDTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    stripe_mask = make_centered_rectangle(
        stripe_width,
        TARGET_HEIGHT,
        0.0,
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="USPSA_Center_Stripe_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=stripe_mask,
        face_layer_thickness=face_layer_thickness,
    )


def create_tuxedo_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    center_width=DEFAULT_TUXEDO_CENTER_WIDTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    tuxedo_mask = make_tuxedo_mask(
        scale,
        face_layer_thickness,
        center_width=center_width,
    )

    return build_hard_cover_target(
        document_name="USPSA_Tuxedo_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=tuxedo_mask,
        face_layer_thickness=face_layer_thickness,
    )


def create_right_half_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    right_half_mask = make_right_half_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="USPSA_Right_Half_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=right_half_mask,
        face_layer_thickness=face_layer_thickness,
    )


def create_left_half_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    left_half_mask = make_left_half_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="USPSA_Left_Half_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=left_half_mask,
        face_layer_thickness=face_layer_thickness,
    )


def create_diagonal_left_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    diagonal_mask = make_diagonal_left_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="USPSA_Diagonal_Left_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=diagonal_mask,
        face_layer_thickness=face_layer_thickness,
    )


def create_diagonal_right_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    diagonal_mask = make_diagonal_right_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="USPSA_Diagonal_Right_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=diagonal_mask,
        face_layer_thickness=face_layer_thickness,
    )


def show_target_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Cardboard Target",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    create_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_body_hard_cover_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Body Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Body hard cover uses face-down split parts.\n"
    )

    create_body_hard_cover_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_lower_half_hard_cover_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Lower Half Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Lower Half hard cover uses face-down split parts.\n"
    )

    create_lower_half_hard_cover_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_center_stripe_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Center Stripe Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Center Stripe hard cover uses face-down split parts.\n"
    )

    create_center_stripe_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_tuxedo_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Tuxedo Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Tuxedo hard cover uses face-down split parts.\n"
    )

    create_tuxedo_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_right_half_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Right Half Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Right Half hard cover uses face-down split parts.\n"
    )

    create_right_half_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_left_half_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Left Half Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Left Half hard cover uses face-down split parts.\n"
    )

    create_left_half_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_diagonal_left_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Diagonal Left Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Diagonal Left hard cover uses face-down split parts.\n"
    )

    create_diagonal_left_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_diagonal_right_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Diagonal Right Hard Cover",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    App.Console.PrintMessage(
        "Diagonal Right hard cover uses face-down split parts.\n"
    )

    create_diagonal_right_target(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


class CreateUSPSATargetCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Cardboard Target",
            "ToolTip": "Create a scaled USPSA cardboard dry fire target",
        }

    def Activated(self):
        show_target_dialog()

    def IsActive(self):
        return True


class CreateUSPSABodyHardCoverCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Body Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 1",
        }

    def Activated(self):
        show_body_hard_cover_dialog()

    def IsActive(self):
        return True


class CreateUSPSALowerHalfHardCoverCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Lower Half Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 5",
        }

    def Activated(self):
        show_lower_half_hard_cover_dialog()

    def IsActive(self):
        return True


class CreateUSPSACenterStripeCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Center Stripe Hard Cover",
            "ToolTip": "Create a USPSA center stripe hard cover target",
        }

    def Activated(self):
        show_center_stripe_dialog()

    def IsActive(self):
        return True


class CreateUSPSATuxedoCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Tuxedo Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 4",
        }

    def Activated(self):
        show_tuxedo_dialog()

    def IsActive(self):
        return True


class CreateUSPSARightHalfCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Right Half Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 6",
        }

    def Activated(self):
        show_right_half_dialog()

    def IsActive(self):
        return True


class CreateUSPSALeftHalfCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Left Half Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 7",
        }

    def Activated(self):
        show_left_half_dialog()

    def IsActive(self):
        return True


class CreateUSPSADiagonalLeftCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Diagonal Left Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 3",
        }

    def Activated(self):
        show_diagonal_left_dialog()

    def IsActive(self):
        return True


class CreateUSPSADiagonalRightCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Diagonal Right Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 2",
        }

    def Activated(self):
        show_diagonal_right_dialog()

    def IsActive(self):
        return True