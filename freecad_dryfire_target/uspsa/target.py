import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.geometry import (
    make_extruded_polygon,
    make_polyline_groove,
    make_rectangle_groove,
)

from freecad_dryfire_target.uspsa.dimensions import (
    C_D_BOUNDARY,
    DEFAULT_GROOVE_DEPTH,
    DEFAULT_GROOVE_WIDTH,
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    LOWER_A_ZONE_BOTTOM,
    LOWER_A_ZONE_HEIGHT,
    LOWER_A_ZONE_WIDTH,
    TARGET_OUTLINE,
    UPPER_A_ZONE_BOTTOM,
    UPPER_A_ZONE_HEIGHT,
    UPPER_A_ZONE_WIDTH,
)


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
    target_shape = make_target_outline(
        scale,
        thickness,
    )

    return add_scoring_grooves(
        target_shape,
        scale,
        thickness,
        groove_width,
        groove_depth,
    )


def add_scoring_grooves(
    target_shape,
    scale,
    thickness,
    groove_width,
    groove_depth,
    face="top",
):
    upper_a_zone = make_rectangle_groove(
        UPPER_A_ZONE_WIDTH,
        UPPER_A_ZONE_HEIGHT,
        UPPER_A_ZONE_BOTTOM,
        scale,
        thickness,
        groove_width,
        groove_depth,
        face=face,
    )

    lower_a_zone = make_rectangle_groove(
        LOWER_A_ZONE_WIDTH,
        LOWER_A_ZONE_HEIGHT,
        LOWER_A_ZONE_BOTTOM,
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


def create_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
):
    document = App.newDocument(
        "USPSA_DryFire_Target"
    )

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

    target.ViewObject.ShapeColor = (
        0.76,
        0.56,
        0.32,
    )

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewTop()
    view.fitAll()

    return target