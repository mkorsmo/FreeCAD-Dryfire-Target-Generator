import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.geometry import (
    make_extruded_polygon,
)

from freecad_dryfire_target.ipsc.dimensions import (
    DEFAULT_GROOVE_DEPTH,
    DEFAULT_GROOVE_WIDTH,
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    TARGET_OUTLINE,
)

from freecad_dryfire_target.ipsc.target import (
    MOUNT_NONE,
    add_scoring_grooves,
    make_target_mount,
)


DEFAULT_FACE_LAYER_THICKNESS = 0.4


def make_classic_2_mask(
    scale,
    thickness,
):
    """
    IPSC Classic Hardcover Version 2.

    Hard cover occupies the right side of the finished target.
    The diagonal runs from the upper-right corner of the top flat
    down toward the lower-left corner of the bottom flat.
    """
    points = [
        (300.0, -50.0),
        (300.0, 650.0),
        (75.0, 570.0),
        (-75.0, 0.0),
    ]

    return make_extruded_polygon(
        points,
        scale,
        thickness,
    )


def make_classic_3_mask(
    scale,
    thickness,
):
    """
    IPSC Classic Hardcover Version 3.

    Hard cover occupies the left side of the finished target.
    The diagonal runs from the upper-left corner of the top flat
    down toward the lower-right corner of the bottom flat.
    """
    points = [
        (-300.0, 650.0),
        (-300.0, -50.0),
        (75.0, 0.0),
        (-75.0, 570.0),
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
    mount=MOUNT_NONE,
):
    document = App.newDocument(
        document_name
    )

    if thickness <= 0.4:
        face_layer_thickness = thickness / 2
    else:
        face_layer_thickness = min(
            face_layer_thickness,
            thickness - 0.2,
        )

    back_thickness = (
        thickness - face_layer_thickness
    )

    back_shape = make_extruded_polygon(
        TARGET_OUTLINE,
        scale,
        back_thickness,
        z_offset=face_layer_thickness,
    )

    mount_shape = make_target_mount(
        mount,
        scale,
        thickness,
    )

    if mount_shape is not None:
        back_shape = back_shape.fuse(
            mount_shape
        ).removeSplitter()

    face_layer = make_extruded_polygon(
        TARGET_OUTLINE,
        scale,
        face_layer_thickness,
    )

    hard_cover_face = face_layer.common(
        hard_cover_mask
    )

    cardboard_face = face_layer.cut(
        hard_cover_face
    )

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

    rotation_center = App.Vector(
        0,
        0,
        0,
    )

    rotation_axis = App.Vector(
        0,
        0,
        1,
    )

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
        "IPSC_Back",
    )

    back.Label = "IPSC Back"
    back.Shape = back_shape
    back.ViewObject.ShapeColor = (
        0.76,
        0.56,
        0.32,
    )

    cardboard = document.addObject(
        "Part::Feature",
        "IPSC_Cardboard_Face",
    )

    cardboard.Label = "IPSC Cardboard Face"
    cardboard.Shape = cardboard_face
    cardboard.ViewObject.ShapeColor = (
        0.76,
        0.56,
        0.32,
    )

    hard_cover = document.addObject(
        "Part::Feature",
        "IPSC_HardCover_Face",
    )

    hard_cover.Label = "IPSC Hard Cover Face"
    hard_cover.Shape = hard_cover_face
    hard_cover.ViewObject.ShapeColor = (
        0.1,
        0.1,
        0.1,
    )

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewBottom()
    view.fitAll()

    return (
        back,
        cardboard,
        hard_cover,
    )


def create_classic_2_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
):
    diagonal_mask = make_classic_2_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="IPSC_Classic_2_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=diagonal_mask,
        face_layer_thickness=face_layer_thickness,
        mount=mount,
    )


def create_classic_3_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
):
    diagonal_mask = make_classic_3_mask(
        scale,
        face_layer_thickness,
    )

    return build_hard_cover_target(
        document_name="IPSC_Classic_3_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=diagonal_mask,
        face_layer_thickness=face_layer_thickness,
        mount=mount,
    )
