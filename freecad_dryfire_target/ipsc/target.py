import math

import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.geometry import (
    make_extruded_polygon,
    make_polyline_groove,
)

from freecad_dryfire_target.ipsc.dimensions import (
    A_BOUNDARY,
    C_D_BOTTOM_LEFT,
    C_D_BOTTOM_RIGHT,
    C_D_LOWER_LEFT,
    C_D_LOWER_RIGHT,
    C_D_UPPER_LEFT,
    C_D_UPPER_RIGHT,
    DEFAULT_GROOVE_DEPTH,
    DEFAULT_GROOVE_WIDTH,
    DEFAULT_INCLUDE_PERIMETER,
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    NON_SCORING_BORDER,
    TARGET_OUTLINE,
)


TARGET_COLOR = (
    0.76,
    0.56,
    0.32,
)


def line_intersection(
    point_a,
    direction_a,
    point_b,
    direction_b,
):
    ax, ay = point_a
    adx, ady = direction_a

    bx, by = point_b
    bdx, bdy = direction_b

    denominator = (
        adx * bdy
        - ady * bdx
    )

    if abs(denominator) < 0.000001:
        raise ValueError(
            "Cannot intersect parallel polygon edges."
        )

    offset_x = bx - ax
    offset_y = by - ay

    distance = (
        offset_x * bdy
        - offset_y * bdx
    ) / denominator

    return (
        ax + distance * adx,
        ay + distance * ady,
    )


def make_inset_polygon(
    points,
    inset,
):
    offset_lines = []

    for index in range(
        len(points)
    ):
        x1, y1 = points[index]
        x2, y2 = points[
            (index + 1)
            % len(points)
        ]

        dx = x2 - x1
        dy = y2 - y1

        length = math.hypot(
            dx,
            dy,
        )

        if length <= 0:
            raise ValueError(
                "Target outline contains a zero-length edge."
            )

        inward_x = (
            -dy / length
        )
        inward_y = (
            dx / length
        )

        offset_lines.append(
            (
                (
                    x1
                    + inward_x
                    * inset,
                    y1
                    + inward_y
                    * inset,
                ),
                (
                    dx,
                    dy,
                ),
            )
        )

    inset_points = []

    for index in range(
        len(points)
    ):
        previous_line = offset_lines[
            index - 1
        ]
        current_line = offset_lines[
            index
        ]

        inset_points.append(
            line_intersection(
                previous_line[0],
                previous_line[1],
                current_line[0],
                current_line[1],
            )
        )

    return inset_points


def make_scoring_border():
    return make_inset_polygon(
        TARGET_OUTLINE,
        NON_SCORING_BORDER,
    )


def make_c_d_boundary():
    scoring_border = (
        make_scoring_border()
    )

    top_right = scoring_border[4]
    top_left = scoring_border[5]

    return [
        C_D_BOTTOM_LEFT,
        C_D_BOTTOM_RIGHT,
        C_D_LOWER_RIGHT,
        C_D_UPPER_RIGHT,
        top_right,
        top_left,
        C_D_UPPER_LEFT,
        C_D_LOWER_LEFT,
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


def add_scoring_grooves(
    target_shape,
    scale,
    thickness,
    groove_width,
    groove_depth,
    include_perimeter=DEFAULT_INCLUDE_PERIMETER,
    face="top",
):
    a_boundary = make_polyline_groove(
        A_BOUNDARY,
        scale,
        thickness,
        groove_width,
        groove_depth,
        face=face,
    )

    c_d_boundary = make_polyline_groove(
        make_c_d_boundary(),
        scale,
        thickness,
        groove_width,
        groove_depth,
        face=face,
    )

    target_shape = (
        target_shape.cut(
            a_boundary
        )
    )

    target_shape = (
        target_shape.cut(
            c_d_boundary
        )
    )

    if include_perimeter:
        scoring_border = (
            make_polyline_groove(
                make_scoring_border(),
                scale,
                thickness,
                groove_width,
                groove_depth,
                face=face,
            )
        )

        target_shape = (
            target_shape.cut(
                scoring_border
            )
        )

    return target_shape


def make_scored_target_shape(
    scale,
    thickness,
    groove_width,
    groove_depth,
    include_perimeter=DEFAULT_INCLUDE_PERIMETER,
):
    target_shape = (
        make_target_outline(
            scale,
            thickness,
        )
    )

    return add_scoring_grooves(
        target_shape,
        scale,
        thickness,
        groove_width,
        groove_depth,
        include_perimeter=include_perimeter,
    )


def create_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    include_perimeter=DEFAULT_INCLUDE_PERIMETER,
):
    document = App.newDocument(
        "IPSC_DryFire_Target"
    )

    target_shape = (
        make_scored_target_shape(
            scale,
            thickness,
            groove_width,
            groove_depth,
            include_perimeter=include_perimeter,
        )
    )

    target = document.addObject(
        "Part::Feature",
        "IPSC_Target",
    )

    target.Label = (
        "IPSC Cardboard Target"
    )

    target.Shape = target_shape

    target.ViewObject.ShapeColor = (
        TARGET_COLOR
    )

    document.recompute()

    view = (
        Gui.activeDocument()
        .activeView()
    )

    view.viewTop()
    view.fitAll()

    return target
