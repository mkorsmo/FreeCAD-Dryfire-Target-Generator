import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.geometry import (
    make_extruded_polygon,
    make_polyline_groove,
    make_rectangle_groove,
)

from freecad_dryfire_target.mounts import (
    make_vertical_pvc_clips,
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


VERTICAL_PVC_TEST_CLIP_POSITIONS = [
    (0.0, 150.0),
    (0.0, 450.0),
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


def create_vertical_pvc_mount_test_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
):
    """
    Create a full USPSA target with two vertical 1/2-inch PVC clips.

    This is intentionally a test-only creator. The target face is at
    Z=0 and the clips grow from the back at Z=thickness so the entire
    part can be printed face-down.
    """
    document = App.newDocument(
        "USPSA_Vertical_PVC_Mount_Test"
    )

    target_shape = make_target_outline(
        scale,
        thickness,
    )

    target_shape = add_scoring_grooves(
        target_shape,
        scale,
        thickness,
        groove_width,
        groove_depth,
        face="bottom",
    )

    clip_positions = [
        (
            x * scale,
            y * scale,
        )
        for x, y in VERTICAL_PVC_TEST_CLIP_POSITIONS
    ]

    clips = make_vertical_pvc_clips(
        positions=clip_positions,
        z_offset=thickness,
    )

    target_shape = target_shape.fuse(
        clips
    ).removeSplitter()

    target_shape.rotate(
        App.Vector(0, 0, 0),
        App.Vector(0, 0, 1),
        180,
    )

    target = document.addObject(
        "Part::Feature",
        "USPSA_Vertical_PVC_Mount_Test",
    )

    target.Label = (
        "USPSA Vertical 1/2 PVC Mount Test"
    )

    target.Shape = target_shape

    target.ViewObject.ShapeColor = (
        0.76,
        0.56,
        0.32,
    )

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewBottom()
    view.fitAll()

    return target
