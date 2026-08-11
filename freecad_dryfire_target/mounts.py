import FreeCAD as App
import FreeCADGui as Gui
import Part


PVC_HALF_INCH_OD = 21.34

DEFAULT_DIAMETRAL_CLEARANCE = 0.40
DEFAULT_CLIP_LENGTH = 20.0
DEFAULT_WALL_THICKNESS = 2.60
DEFAULT_ARM_HEIGHT = 17.0
DEFAULT_HOOK_PROJECTION = 1.00
DEFAULT_HOOK_CENTER_HEIGHT = 13.50
DEFAULT_HOOK_HEIGHT = 4.0
DEFAULT_PAD_THICKNESS = 2.00
DEFAULT_PAD_MARGIN_X = 2.5
DEFAULT_PAD_MARGIN_Y = 3.0
DEFAULT_GUSSET_HEIGHT = 4.0
DEFAULT_GUSSET_PROJECTION = 2.0

DEFAULT_TEST_PLATE_WIDTH = 44.0
DEFAULT_TEST_PLATE_LENGTH = 36.0
DEFAULT_TEST_PLATE_THICKNESS = 1.20


def make_xz_prism(
    points,
    length,
    y_center=0.0,
):
    vectors = [
        App.Vector(
            x,
            y_center - length / 2,
            z,
        )
        for x, z in points
    ]

    vectors.append(vectors[0])

    wire = Part.makePolygon(vectors)
    face = Part.Face(wire)

    return face.extrude(
        App.Vector(
            0,
            length,
            0,
        )
    )


def make_vertical_pvc_clip(
    pvc_od=PVC_HALF_INCH_OD,
    diametral_clearance=DEFAULT_DIAMETRAL_CLEARANCE,
    clip_length=DEFAULT_CLIP_LENGTH,
    wall_thickness=DEFAULT_WALL_THICKNESS,
    arm_height=DEFAULT_ARM_HEIGHT,
    hook_projection=DEFAULT_HOOK_PROJECTION,
    hook_center_height=DEFAULT_HOOK_CENTER_HEIGHT,
    hook_height=DEFAULT_HOOK_HEIGHT,
    pad_thickness=DEFAULT_PAD_THICKNESS,
    pad_margin_x=DEFAULT_PAD_MARGIN_X,
    pad_margin_y=DEFAULT_PAD_MARGIN_Y,
    z_offset=0.0,
    gusset_height=DEFAULT_GUSSET_HEIGHT,
    gusset_projection=DEFAULT_GUSSET_PROJECTION,
):
    """
    Create a reinforced, support-free snap clip for nominal 1/2-inch PVC.

    The pipe axis runs along Y, so on the back of an upright target
    this is the VERTICAL pipe orientation.

    The opening faces +Z, away from the target backing, which allows
    the target to remain face-down during printing.

    The proven PVC clearance and hook geometry are retained. V1 adds
    a slightly thicker pad and arms, a little more clip length, and
    external triangular gussets at the arm roots.
    """
    inner_gap = pvc_od + diametral_clearance

    inner_left_x = -inner_gap / 2
    inner_right_x = inner_gap / 2

    left_outer_x = (
        inner_left_x - wall_thickness
    )

    right_outer_x = (
        inner_right_x + wall_thickness
    )

    pad_width = (
        inner_gap
        + wall_thickness * 2
        + pad_margin_x * 2
    )

    pad_length = (
        clip_length
        + pad_margin_y * 2
    )

    pad = Part.makeBox(
        pad_width,
        pad_length,
        pad_thickness,
        App.Vector(
            -pad_width / 2,
            -pad_length / 2,
            z_offset,
        ),
    )

    arm_z = z_offset + pad_thickness

    left_arm = Part.makeBox(
        wall_thickness,
        clip_length,
        arm_height,
        App.Vector(
            left_outer_x,
            -clip_length / 2,
            arm_z,
        ),
    )

    right_arm = Part.makeBox(
        wall_thickness,
        clip_length,
        arm_height,
        App.Vector(
            inner_right_x,
            -clip_length / 2,
            arm_z,
        ),
    )

    hook_bottom = (
        arm_z
        + hook_center_height
        - hook_height / 2
    )

    hook_center = (
        arm_z
        + hook_center_height
    )

    hook_top = (
        arm_z
        + hook_center_height
        + hook_height / 2
    )

    left_hook = make_xz_prism(
        [
            (
                inner_left_x,
                hook_bottom,
            ),
            (
                inner_left_x
                + hook_projection,
                hook_center,
            ),
            (
                inner_left_x,
                hook_top,
            ),
        ],
        clip_length,
    )

    right_hook = make_xz_prism(
        [
            (
                inner_right_x,
                hook_bottom,
            ),
            (
                inner_right_x
                - hook_projection,
                hook_center,
            ),
            (
                inner_right_x,
                hook_top,
            ),
        ],
        clip_length,
    )

    left_gusset = make_xz_prism(
        [
            (
                left_outer_x,
                arm_z,
            ),
            (
                left_outer_x
                - gusset_projection,
                arm_z,
            ),
            (
                left_outer_x,
                arm_z
                + gusset_height,
            ),
        ],
        clip_length,
    )

    right_gusset = make_xz_prism(
        [
            (
                right_outer_x,
                arm_z,
            ),
            (
                right_outer_x
                + gusset_projection,
                arm_z,
            ),
            (
                right_outer_x,
                arm_z
                + gusset_height,
            ),
        ],
        clip_length,
    )

    clip = pad.fuse(left_arm)
    clip = clip.fuse(right_arm)
    clip = clip.fuse(left_hook)
    clip = clip.fuse(right_hook)
    clip = clip.fuse(left_gusset)
    clip = clip.fuse(right_gusset)

    return clip.removeSplitter()


def make_vertical_pvc_clips(
    positions,
    z_offset,
    pvc_od=PVC_HALF_INCH_OD,
    diametral_clearance=DEFAULT_DIAMETRAL_CLEARANCE,
):
    """
    Create multiple vertical PVC clips at physical X/Y positions.

    Positions are supplied in millimeters. The clip geometry itself
    is not scaled because the PVC remains a fixed physical size.
    """
    clips = None

    for x, y in positions:
        clip = make_vertical_pvc_clip(
            pvc_od=pvc_od,
            diametral_clearance=diametral_clearance,
            z_offset=z_offset,
        )

        clip.translate(
            App.Vector(
                x,
                y,
                0,
            )
        )

        if clips is None:
            clips = clip
        else:
            clips = clips.fuse(clip)

    if clips is None:
        raise ValueError(
            "At least one clip position is required."
        )

    return clips.removeSplitter()


def create_vertical_pvc_clip_test(
    pvc_od=PVC_HALF_INCH_OD,
    diametral_clearance=DEFAULT_DIAMETRAL_CLEARANCE,
):
    """
    Create a small printable test coupon for the reinforced V1 clip.
    """
    document = App.newDocument(
        "Vertical_PVC_Clip_Test"
    )

    plate = Part.makeBox(
        DEFAULT_TEST_PLATE_WIDTH,
        DEFAULT_TEST_PLATE_LENGTH,
        DEFAULT_TEST_PLATE_THICKNESS,
        App.Vector(
            -DEFAULT_TEST_PLATE_WIDTH / 2,
            -DEFAULT_TEST_PLATE_LENGTH / 2,
            0,
        ),
    )

    clip = make_vertical_pvc_clip(
        pvc_od=pvc_od,
        diametral_clearance=diametral_clearance,
        z_offset=DEFAULT_TEST_PLATE_THICKNESS,
    )

    coupon_shape = (
        plate
        .fuse(clip)
        .removeSplitter()
    )

    coupon = document.addObject(
        "Part::Feature",
        "Vertical_PVC_Clip_Test",
    )

    coupon.Label = (
        "Vertical 1/2 PVC Clip Test - Reinforced V1"
    )

    coupon.Shape = coupon_shape

    coupon.addProperty(
        "App::PropertyLength",
        "PVCOutsideDiameter",
        "PVC Clip",
    )

    coupon.addProperty(
        "App::PropertyLength",
        "DiametralClearance",
        "PVC Clip",
    )

    coupon.addProperty(
        "App::PropertyLength",
        "ClipLength",
        "PVC Clip",
    )

    coupon.addProperty(
        "App::PropertyLength",
        "WallThickness",
        "PVC Clip",
    )

    coupon.addProperty(
        "App::PropertyLength",
        "HookProjection",
        "PVC Clip",
    )

    coupon.addProperty(
        "App::PropertyLength",
        "PadThickness",
        "PVC Clip",
    )

    coupon.addProperty(
        "App::PropertyLength",
        "GussetHeight",
        "PVC Clip",
    )

    coupon.addProperty(
        "App::PropertyLength",
        "GussetProjection",
        "PVC Clip",
    )

    coupon.PVCOutsideDiameter = pvc_od
    coupon.DiametralClearance = (
        diametral_clearance
    )
    coupon.ClipLength = DEFAULT_CLIP_LENGTH
    coupon.WallThickness = (
        DEFAULT_WALL_THICKNESS
    )
    coupon.HookProjection = (
        DEFAULT_HOOK_PROJECTION
    )
    coupon.PadThickness = (
        DEFAULT_PAD_THICKNESS
    )
    coupon.GussetHeight = (
        DEFAULT_GUSSET_HEIGHT
    )
    coupon.GussetProjection = (
        DEFAULT_GUSSET_PROJECTION
    )

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewAxonometric()
    view.fitAll()

    return coupon
