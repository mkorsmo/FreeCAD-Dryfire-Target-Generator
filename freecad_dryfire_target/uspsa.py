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

def create_center_stripe_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    stripe_width=DEFAULT_CENTER_STRIPE_WIDTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
):
    document = App.newDocument("USPSA_Center_Stripe_Target")

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

    stripe_mask = make_centered_rectangle(
        stripe_width,
        TARGET_HEIGHT,
        0.0,
        scale,
        face_layer_thickness,
    )

    hard_cover_face = face_layer.common(stripe_mask)
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
    view.fitAll()

    return back, cardboard, hard_cover

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