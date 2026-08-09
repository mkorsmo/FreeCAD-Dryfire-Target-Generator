import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.geometry import (
    make_extruded_polygon,
    make_polyline_groove,
    make_rectangle_groove,
)


SCALE = 1 / 3

THICKNESS = 1.2
GROOVE_WIDTH = 0.6
GROOVE_DEPTH = 0.3


TARGET_OUTLINE = [
    (-150.0, 0.0),
    (150.0, 0.0),
    (225.0, 200.0),
    (225.0, 550.0),
    (150.0, 600.0),
    (75.0, 600.0),
    (75.0, 750.0),
    (-75.0, 750.0),
    (-75.0, 600.0),
    (-150.0, 600.0),
    (-225.0, 550.0),
    (-225.0, 200.0),
]


C_D_BOUNDARY = [
    (-75.0, 600.0),
    (-150.0, 550.0),
    (-150.0, 270.0),
    (-100.0, 200.0),
    (100.0, 200.0),
    (150.0, 270.0),
    (150.0, 550.0),
    (75.0, 600.0),
]


def make_target_outline():
    return make_extruded_polygon(
        TARGET_OUTLINE,
        SCALE,
        THICKNESS,
    )


def create_target():
    document = App.newDocument("USPSA_DryFire_Target")

    target_shape = make_target_outline()

    upper_a_zone = make_rectangle_groove(
        100.0,
        50.0,
        675.0,
        SCALE,
        THICKNESS,
        GROOVE_WIDTH,
        GROOVE_DEPTH,
    )

    lower_a_zone = make_rectangle_groove(
        150.0,
        280.0,
        270.0,
        SCALE,
        THICKNESS,
        GROOVE_WIDTH,
        GROOVE_DEPTH,
    )

    c_d_boundary = make_polyline_groove(
        C_D_BOUNDARY,
        SCALE,
        THICKNESS,
        GROOVE_WIDTH,
        GROOVE_DEPTH,
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

    target.Scale = SCALE
    target.Thickness = THICKNESS
    target.GrooveWidth = GROOVE_WIDTH
    target.GrooveDepth = GROOVE_DEPTH

    target.ViewObject.ShapeColor = (0.76, 0.56, 0.32)

    document.recompute()

    Gui.activeDocument().activeView().viewTop()
    Gui.activeDocument().activeView().fitAll()

    return target


class CreateUSPSATargetCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Cardboard Target",
            "ToolTip": "Create a scaled USPSA cardboard dry fire target",
        }

    def Activated(self):
        create_target()

    def IsActive(self):
        return True