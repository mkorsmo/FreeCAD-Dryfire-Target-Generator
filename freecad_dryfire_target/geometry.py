import math

import FreeCAD as App
import Part


def scale_value(value, scale_factor):
    return value * scale_factor


def make_extruded_polygon(
    points,
    scale_factor,
    thickness,
    z_offset=0,
):
    vectors = [
        App.Vector(
            scale_value(x, scale_factor),
            scale_value(y, scale_factor),
            0,
        )
        for x, y in points
    ]

    vectors.append(vectors[0])

    wire = Part.makePolygon(vectors)
    face = Part.Face(wire)

    solid = face.extrude(
        App.Vector(
            0,
            0,
            thickness,
        )
    )

    if z_offset:
        solid.translate(
            App.Vector(
                0,
                0,
                z_offset,
            )
        )

    return solid


def make_rectangle_groove(
    width,
    height,
    bottom,
    scale_factor,
    thickness,
    groove_width,
    groove_depth,
    face="top",
):
    width = scale_value(width, scale_factor)
    height = scale_value(height, scale_factor)
    bottom = scale_value(bottom, scale_factor)

    outer_width = width + groove_width
    outer_height = height + groove_width
    inner_width = width - groove_width
    inner_height = height - groove_width

    z = get_groove_z(
        thickness,
        groove_depth,
        face,
    )

    outer = Part.makeBox(
        outer_width,
        outer_height,
        groove_depth,
        App.Vector(
            -outer_width / 2,
            bottom - groove_width / 2,
            z,
        ),
    )

    inner = Part.makeBox(
        inner_width,
        inner_height,
        groove_depth,
        App.Vector(
            -inner_width / 2,
            bottom + groove_width / 2,
            z,
        ),
    )

    return outer.cut(inner)


def make_polyline_groove(
    points,
    scale_factor,
    thickness,
    groove_width,
    groove_depth,
    closed=True,
    face="top",
):
    points = [
        (
            scale_value(x, scale_factor),
            scale_value(y, scale_factor),
        )
        for x, y in points
    ]

    z = get_groove_z(
        thickness,
        groove_depth,
        face,
    )

    radius = groove_width / 2
    groove = None

    segment_count = len(points) if closed else len(points) - 1

    for index in range(segment_count):
        x1, y1 = points[index]
        x2, y2 = points[(index + 1) % len(points)]

        delta_x = x2 - x1
        delta_y = y2 - y1

        length = math.hypot(delta_x, delta_y)
        angle = math.degrees(
            math.atan2(
                delta_y,
                delta_x,
            )
        )

        segment = Part.makeBox(
            length,
            groove_width,
            groove_depth,
            App.Vector(
                0,
                -radius,
                z,
            ),
        )

        segment.rotate(
            App.Vector(0, 0, 0),
            App.Vector(0, 0, 1),
            angle,
        )

        segment.translate(
            App.Vector(
                x1,
                y1,
                0,
            )
        )

        if groove is None:
            groove = segment
        else:
            groove = groove.fuse(segment)

    for x, y in points:
        joint = Part.makeCylinder(
            radius,
            groove_depth,
            App.Vector(
                x,
                y,
                z,
            ),
        )

        groove = groove.fuse(joint)

    return groove

def make_centered_rectangle(
    width,
    height,
    bottom,
    scale_factor,
    thickness,
    z_offset=0,
):
    width = scale_value(width, scale_factor)
    height = scale_value(height, scale_factor)
    bottom = scale_value(bottom, scale_factor)

    return Part.makeBox(
        width,
        height,
        thickness,
        App.Vector(
            -width / 2,
            bottom,
            z_offset,
        ),
    )

def get_groove_z(
    thickness,
    groove_depth,
    face,
):
    if face == "bottom":
        return 0

    return thickness - groove_depth