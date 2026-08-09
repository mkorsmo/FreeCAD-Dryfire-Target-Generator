import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.dialog import TargetSettingsDialog
from freecad_dryfire_target.geometry import (
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

    target_shape = make_target_outline(
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

    target = document.addObject(
        "Part::Feature",
        "USPSA_Target",
    )

    target.Label = "USPSA Cardboard Target"
    target.Shape = target_shape

    target.addProperty(
        "App::PropertyFloat",
        "Scale",
        "Target",
    )

    target.addProperty(
        "App::PropertyLength",
        "Thickness",
        "Target",
    )

    target.addProperty(
        "App::PropertyLength",
        "GrooveWidth",
        "Scoring Lines",
    )

    target.addProperty(
        "App::PropertyLength",
        "GrooveDepth",
        "Scoring Lines",
    )

    target.Scale = scale
    target.Thickness = thickness
    target.GrooveWidth = groove_width
    target.GrooveDepth = groove_depth

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

    if dialog.exec() != QtWidgets.QDialog.Accepted:
        return

    settings = dialog.get_settings()

    create_target(
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