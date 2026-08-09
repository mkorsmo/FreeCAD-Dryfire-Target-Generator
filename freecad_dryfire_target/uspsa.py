import FreeCAD as App
import FreeCADGui as Gui
import Part


SCALE = 1 / 3

THICKNESS = 1.2
GROOVE_WIDTH = 0.6
GROOVE_DEPTH = 0.3


def scaled(value):
    return value * SCALE


def make_target_outline():
    points = [
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

    vectors = [
        App.Vector(
            scaled(x),
            scaled(y),
            0,
        )
        for x, y in points
    ]

    vectors.append(vectors[0])

    wire = Part.makePolygon(vectors)
    face = Part.Face(wire)

    return face.extrude(
        App.Vector(
            0,
            0,
            THICKNESS,
        )
    )


def make_rectangle_groove(width, height, bottom):
    width = scaled(width)
    height = scaled(height)
    bottom = scaled(bottom)

    outer_width = width + GROOVE_WIDTH
    outer_height = height + GROOVE_WIDTH

    inner_width = width - GROOVE_WIDTH
    inner_height = height - GROOVE_WIDTH

    outer = Part.makeBox(
        outer_width,
        outer_height,
        GROOVE_DEPTH,
        App.Vector(
            -outer_width / 2,
            bottom - GROOVE_WIDTH / 2,
            THICKNESS - GROOVE_DEPTH,
        ),
    )

    inner = Part.makeBox(
        inner_width,
        inner_height,
        GROOVE_DEPTH,
        App.Vector(
            -inner_width / 2,
            bottom + GROOVE_WIDTH / 2,
            THICKNESS - GROOVE_DEPTH,
        ),
    )

    return outer.cut(inner)


def create_target():
    document = App.newDocument("USPSA_DryFire_Target")

    target_shape = make_target_outline()

    upper_a_zone = make_rectangle_groove(
        100.0,
        50.0,
        675.0,
    )

    lower_a_zone = make_rectangle_groove(
        150.0,
        280.0,
        270.0,
    )

    target_shape = target_shape.cut(upper_a_zone)
    target_shape = target_shape.cut(lower_a_zone)

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