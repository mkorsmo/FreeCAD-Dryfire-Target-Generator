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


MOUNT_NONE = "none"
MOUNT_VERTICAL_PVC = "vertical_pvc"

MOUNT_LAYOUT_TOP_BOTTOM = "top_bottom"
MOUNT_LAYOUT_TOP = "top"
MOUNT_LAYOUT_MIDDLE = "middle"
MOUNT_LAYOUT_BOTTOM = "bottom"

VERTICAL_PVC_CLIP_LAYOUTS = {
    MOUNT_LAYOUT_TOP: [
        (0.0, 450.0),
    ],
    MOUNT_LAYOUT_MIDDLE: [
        (0.0, 300.0),
    ],
    MOUNT_LAYOUT_BOTTOM: [
        (0.0, 150.0),
    ],
    MOUNT_LAYOUT_TOP_BOTTOM: [
        (0.0, 450.0),
        (0.0, 150.0),
    ],
}


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


def make_target_mount(
    mount,
    scale,
    thickness,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
):
    if mount in (
        None,
        MOUNT_NONE,
    ):
        return None

    if mount == MOUNT_VERTICAL_PVC:
        full_scale_positions = (
            VERTICAL_PVC_CLIP_LAYOUTS.get(
                mount_layout
            )
        )

        if full_scale_positions is None:
            raise ValueError(
                f"Unknown vertical PVC clip layout: {mount_layout}"
            )

        clip_positions = [
            (
                x * scale,
                y * scale,
            )
            for x, y in full_scale_positions
        ]

        return make_vertical_pvc_clips(
            positions=clip_positions,
            z_offset=thickness,
        )

    raise ValueError(
        f"Unknown USPSA mount type: {mount}"
    )


def create_target(
    scale=DEFAULT_SCALE,
    thickness=DEFAULT_THICKNESS,
    groove_width=DEFAULT_GROOVE_WIDTH,
    groove_depth=DEFAULT_GROOVE_DEPTH,
    mount=MOUNT_NONE,
    mount_layout=MOUNT_LAYOUT_TOP_BOTTOM,
):
    document = App.newDocument(
        "USPSA_DryFire_Target"
    )

    if mount == MOUNT_NONE:
        target_shape = make_scored_target_shape(
            scale,
            thickness,
            groove_width,
            groove_depth,
        )

        view_face = "top"

    else:
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

        mount_shape = make_target_mount(
            mount,
            scale,
            thickness,
            mount_layout=mount_layout,
        )

        target_shape = target_shape.fuse(
            mount_shape
        ).removeSplitter()

        target_shape.rotate(
            App.Vector(0, 0, 0),
            App.Vector(0, 0, 1),
            180,
        )

        view_face = "bottom"

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

    if view_face == "bottom":
        view.viewBottom()
    else:
        view.viewTop()

    view.fitAll()

    return target