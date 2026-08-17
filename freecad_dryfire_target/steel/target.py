import math

import FreeCAD as App
import FreeCADGui as Gui
import Part

from freecad_dryfire_target.steel.dimensions import (
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    TARGET_TYPES,
    USPSA_MINI_POPPER_BODY_CENTER_Y,
    USPSA_MINI_POPPER_BODY_RADIUS,
    USPSA_MINI_POPPER_STEM_BASE_WIDTH,
    USPSA_MINI_POPPER_STEM_JOIN_WIDTH,
    USPSA_MINI_POPPER_TOTAL_HEIGHT,
    USPSA_POPPER_BODY_CENTER_Y,
    USPSA_POPPER_BODY_RADIUS,
    USPSA_POPPER_HEAD_RADIUS,
    USPSA_POPPER_STEM_BASE_WIDTH,
    USPSA_POPPER_STEM_JOIN_WIDTH,
    USPSA_POPPER_TOTAL_HEIGHT,
)


STEEL_COLOR = (
    0.72,
    0.72,
    0.72,
)


def scaled_point(
    x,
    y,
    scale,
):
    return App.Vector(
        x * scale,
        y * scale,
        0,
    )


def make_line(
    x1,
    y1,
    x2,
    y2,
    scale,
):
    return Part.makeLine(
        scaled_point(
            x1,
            y1,
            scale,
        ),
        scaled_point(
            x2,
            y2,
            scale,
        ),
    )


def make_arc(
    x1,
    y1,
    xm,
    ym,
    x2,
    y2,
    scale,
):
    return Part.Arc(
        scaled_point(
            x1,
            y1,
            scale,
        ),
        scaled_point(
            xm,
            ym,
            scale,
        ),
        scaled_point(
            x2,
            y2,
            scale,
        ),
    ).toShape()


def make_face_from_edges(
    edges,
):
    wire = Part.Wire(
        edges
    )

    return Part.Face(
        wire
    )


def make_circle_face(
    center_x,
    center_y,
    radius,
    scale,
):
    circle = Part.makeCircle(
        radius * scale,
        scaled_point(
            center_x,
            center_y,
            scale,
        ),
    )

    return Part.Face(
        Part.Wire(
            [circle]
        )
    )


def make_round_plate(
    diameter,
    scale,
    thickness,
):
    radius = (
        diameter
        * scale
        / 2
    )

    return Part.makeCylinder(
        radius,
        thickness,
        App.Vector(
            0,
            radius,
            0,
        ),
    )


def make_square_plate(
    side,
    scale,
    thickness,
):
    size = (
        side
        * scale
    )

    return Part.makeBox(
        size,
        size,
        thickness,
        App.Vector(
            -size / 2,
            0,
            0,
        ),
    )


def make_uspsa_popper_face(
    total_height,
    body_center_y,
    body_radius,
    head_radius,
    stem_base_width,
    stem_join_width,
    scale,
):
    stem_base_half_width = (
        stem_base_width / 2
    )
    stem_join_half_width = (
        stem_join_width / 2
    )

    lower_join_y = (
        body_center_y
        - math.sqrt(
            (body_radius ** 2)
            - (stem_join_half_width ** 2)
        )
    )

    upper_join_y = (
        body_center_y
        + math.sqrt(
            (body_radius ** 2)
            - (head_radius ** 2)
        )
    )

    head_arc_start_y = (
        total_height
        - head_radius
    )

    edges = [
        make_line(
            -stem_base_half_width,
            0,
            stem_base_half_width,
            0,
            scale,
        ),
        make_line(
            stem_base_half_width,
            0,
            stem_join_half_width,
            lower_join_y,
            scale,
        ),
        make_arc(
            stem_join_half_width,
            lower_join_y,
            body_radius,
            body_center_y,
            head_radius,
            upper_join_y,
            scale,
        ),
        make_line(
            head_radius,
            upper_join_y,
            head_radius,
            head_arc_start_y,
            scale,
        ),
        make_arc(
            head_radius,
            head_arc_start_y,
            0,
            total_height,
            -head_radius,
            head_arc_start_y,
            scale,
        ),
        make_line(
            -head_radius,
            head_arc_start_y,
            -head_radius,
            upper_join_y,
            scale,
        ),
        make_arc(
            -head_radius,
            upper_join_y,
            -body_radius,
            body_center_y,
            -stem_join_half_width,
            lower_join_y,
            scale,
        ),
        make_line(
            -stem_join_half_width,
            lower_join_y,
            -stem_base_half_width,
            0,
            scale,
        ),
    ]

    return make_face_from_edges(
        edges
    )


def make_uspsa_mini_popper_face(
    body_center_y,
    body_radius,
    stem_base_width,
    stem_join_width,
    scale,
):
    stem_base_half_width = (
        stem_base_width / 2
    )
    stem_join_half_width = (
        stem_join_width / 2
    )

    lower_join_y = (
        body_center_y
        - math.sqrt(
            (body_radius ** 2)
            - (stem_join_half_width ** 2)
        )
    )

    edges = [
        make_line(
            -stem_base_half_width,
            0,
            stem_base_half_width,
            0,
            scale,
        ),
        make_line(
            stem_base_half_width,
            0,
            stem_join_half_width,
            lower_join_y,
            scale,
        ),
        make_arc(
            stem_join_half_width,
            lower_join_y,
            0,
            body_center_y + body_radius,
            -stem_join_half_width,
            lower_join_y,
            scale,
        ),
        make_line(
            -stem_join_half_width,
            lower_join_y,
            -stem_base_half_width,
            0,
            scale,
        ),
    ]

    return make_face_from_edges(
        edges
    )


def make_uspsa_popper(
    scale,
    thickness,
):
    face = make_uspsa_popper_face(
        total_height=USPSA_POPPER_TOTAL_HEIGHT,
        body_center_y=USPSA_POPPER_BODY_CENTER_Y,
        body_radius=USPSA_POPPER_BODY_RADIUS,
        head_radius=USPSA_POPPER_HEAD_RADIUS,
        stem_base_width=USPSA_POPPER_STEM_BASE_WIDTH,
        stem_join_width=USPSA_POPPER_STEM_JOIN_WIDTH,
        scale=scale,
    )

    return face.extrude(
        App.Vector(
            0,
            0,
            thickness,
        )
    )


def make_uspsa_mini_popper(
    scale,
    thickness,
):
    face = make_uspsa_mini_popper_face(
        body_center_y=USPSA_MINI_POPPER_BODY_CENTER_Y,
        body_radius=USPSA_MINI_POPPER_BODY_RADIUS,
        stem_base_width=USPSA_MINI_POPPER_STEM_BASE_WIDTH,
        stem_join_width=USPSA_MINI_POPPER_STEM_JOIN_WIDTH,
        scale=scale,
    )

    return face.extrude(
        App.Vector(
            0,
            0,
            thickness,
        )
    )


def make_steel_target(
    target_type,
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
):
    target_info = TARGET_TYPES.get(
        target_type
    )

    if target_info is None:
        raise ValueError(
            f"Unknown steel target type: {target_type}"
        )

    kind = target_info["kind"]

    if kind == "round":
        return make_round_plate(
            target_info["diameter"],
            scale,
            thickness,
        )

    if kind == "square":
        return make_square_plate(
            target_info["side"],
            scale,
            thickness,
        )

    if kind == "uspsa_popper":
        return make_uspsa_popper(
            scale,
            thickness,
        )

    if kind == "uspsa_mini_popper":
        return make_uspsa_mini_popper(
            scale,
            thickness,
        )

    raise ValueError(
        f"Unsupported steel target kind: {kind}"
    )


def create_steel_target(
    target_type,
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
):
    target_info = TARGET_TYPES.get(
        target_type
    )

    if target_info is None:
        raise ValueError(
            f"Unknown steel target type: {target_type}"
        )

    document = App.newDocument(
        "Steel_DryFire_Target"
    )

    target = document.addObject(
        "Part::Feature",
        "Steel_Target",
    )

    target.Label = (
        target_info["label"]
    )

    target.Shape = make_steel_target(
        target_type=target_type,
        scale=scale,
        thickness=thickness,
    )

    target.ViewObject.ShapeColor = (
        STEEL_COLOR
    )

    document.recompute()

    view = (
        Gui.activeDocument()
        .activeView()
    )

    view.viewTop()
    view.fitAll()

    return target
