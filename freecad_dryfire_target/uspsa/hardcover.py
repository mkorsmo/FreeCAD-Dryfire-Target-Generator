import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.geometry import (
    make_centered_rectangle,
    make_extruded_polygon,
)

from freecad_dryfire_target.uspsa.dimensions import (
    DEFAULT_BODY_HARD_COVER_TOP,
    DEFAULT_CENTER_STRIPE_WIDTH,
    DEFAULT_DIAGONAL_BOTTOM_X,
    DEFAULT_DIAGONAL_SHOULDER_X,
    DEFAULT_FACE_LAYER_THICKNESS,
    DEFAULT_GROOVE_DEPTH,
    DEFAULT_GROOVE_WIDTH,
    DEFAULT_LOWER_HALF_HARD_COVER_TOP,
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    DEFAULT_TUXEDO_BODY_TOP,
    DEFAULT_TUXEDO_CENTER_WIDTH,
    TARGET_HEIGHT,
    TARGET_OUTLINE,
)

from freecad_dryfire_target.uspsa.target import (
    MOUNT_LAYOUT_TOP_BOTTOM,
    MOUNT_NONE,
    add_scoring_grooves,
    make_target_mount,
)


def make_body_hard_cover_mask(
    scale,
    thickness,
    body_top=DEFAULT_BODY_HARD_COVER_TOP,
):
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


def make_diagonal_right_mask(
    scale,
    thickness,
    shoulder_x=DEFAULT_DIAGONAL_SHOULDER_X,
    bottom_x=DEFAULT_DIAGONAL_BOTTOM_X,
):
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


def make_diagonal_left_mask(
    scale,
    thickness,
    shoulder_x=DEFAULT_DIAGONAL_SHOULDER_X,
    bottom_x=DEFAULT_DIAGONAL_BOTTOM_X,
):
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


def make_tuxedo_mask(
    scale,
    thickness,
    center_width=DEFAULT_TUXEDO_CENTER_WIDTH,
    body_top=DEFAULT_TUXEDO_BODY_TOP,
):
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


def make_lower_half_hard_cover_mask(
    scale,
    thickness,
    cover_top=DEFAULT_LOWER_HALF_HARD_COVER_TOP,
):
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


def make_right_half_mask(
    scale,
    thickness,
    center_width=DEFAULT_TUXEDO_CENTER_WIDTH,
    body_top=DEFAULT_TUXEDO_BODY_TOP,
):
    half_center_width = center_width / 2

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
    half_center_width = center_width / 2

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


def build_hard_cover_target(
    document_name,
    scale,
    thickness,
    groove_width,
    groove_depth,
    hard_cover_mask,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount_layout=mount_layout,
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
        "USPSA_Back",
    )

    back.Label = "USPSA Back"
    back.Shape = back_shape
    back.ViewObject.ShapeColor = (
        0.76,
        0.56,
        0.32,
    )

    cardboard = document.addObject(
        "Part::Feature",
        "USPSA_Cardboard_Face",
    )

    cardboard.Label = "USPSA Cardboard Face"
    cardboard.Shape = cardboard_face
    cardboard.ViewObject.ShapeColor = (
        0.76,
        0.56,
        0.32,
    )

    hard_cover = document.addObject(
        "Part::Feature",
        "USPSA_HardCover_Face",
    )

    hard_cover.Label = "USPSA Hard Cover Face"
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


def create_body_hard_cover_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount=mount,
        mount_layout=mount_layout,
    )


def create_diagonal_right_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount=mount,
        mount_layout=mount_layout,
    )


def create_diagonal_left_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount=mount,
        mount_layout=mount_layout,
    )


def create_tuxedo_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    center_width=DEFAULT_TUXEDO_CENTER_WIDTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount=mount,
        mount_layout=mount_layout,
    )


def create_lower_half_hard_cover_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
):
    lower_half_mask = (
        make_lower_half_hard_cover_mask(
            scale,
            face_layer_thickness,
        )
    )

    return build_hard_cover_target(
        document_name="USPSA_Lower_Half_Hard_Cover_Target",
        scale=scale,
        thickness=thickness,
        groove_width=groove_width,
        groove_depth=groove_depth,
        hard_cover_mask=lower_half_mask,
        face_layer_thickness=face_layer_thickness,
        mount=mount,
        mount_layout=mount_layout,
    )


def create_right_half_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount=mount,
        mount_layout=mount_layout,
    )


def create_left_half_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount=mount,
        mount_layout=mount_layout,
    )


def create_center_stripe_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    stripe_width=DEFAULT_CENTER_STRIPE_WIDTH,
    face_layer_thickness=DEFAULT_FACE_LAYER_THICKNESS,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
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
        mount=mount,
        mount_layout=mount_layout,
    )