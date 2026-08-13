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
DEFAULT_GUSSET_HEIGHT = DEFAULT_ARM_HEIGHT
DEFAULT_GUSSET_PROJECTION = 2.0

DEFAULT_TEST_PLATE_WIDTH = 44.0
DEFAULT_TEST_PLATE_LENGTH = 36.0
DEFAULT_TEST_PLATE_THICKNESS = 1.20

# Quick-change target hanger
#
# These are physical interface dimensions. They do not scale with
# the target.
HANGER_ENTRY_DIAMETER = 8.0
HANGER_SLOT_WIDTH = 4.5
HANGER_SLOT_LENGTH = 8.0

HANGER_REINFORCEMENT_DIAMETER = 18.0
HANGER_REINFORCEMENT_THICKNESS = 1.2

HANGER_SOCKET_DIAMETRAL_CLEARANCE = 0.30
HANGER_SOCKET_OUTER_DIAMETER = 36.0
HANGER_SOCKET_HEIGHT = 34.0
HANGER_SOCKET_DEPTH = 30.0
HANGER_SOCKET_LEAD_IN_HEIGHT = 2.0
HANGER_SOCKET_LEAD_IN_CLEARANCE = 0.8

HANGER_BOSS_WIDTH = 16.0
HANGER_BOSS_HEIGHT = 18.0
HANGER_BOSS_PROJECTION = 5.0
HANGER_BOSS_EMBED_DEPTH = 3.0

HANGER_PEG_CENTER_HEIGHT = 25.0

HANGER_PEG_ROOT_DIAMETER = 10.0
HANGER_PEG_ROOT_LENGTH = 2.0
HANGER_PEG_TAPER_LENGTH = 1.5

HANGER_PEG_SHAFT_DIAMETER = 4.0
HANGER_PEG_SHAFT_LENGTH = 3.0

HANGER_PEG_HEAD_DIAMETER = 7.0
HANGER_PEG_HEAD_THICKNESS = 1.5

HANGER_TEST_COUPON_WIDTH = 30.0
HANGER_TEST_COUPON_HEIGHT = 32.0
HANGER_TEST_COUPON_THICKNESS = 1.2
HANGER_TEST_OBJECT_SPACING = 55.0


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
    full-height tapered external gussets along the clip arms.
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
        "Vertical 1/2 PVC Clip Test - Reinforced V1 Full Gusset"
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

def make_hanger_keyhole_cut(
    entry_diameter=HANGER_ENTRY_DIAMETER,
    slot_width=HANGER_SLOT_WIDTH,
    slot_length=HANGER_SLOT_LENGTH,
    thickness=HANGER_TEST_COUPON_THICKNESS,
    z_offset=0.0,
):
    """
    Create the fixed-size target-side keyhole cut.

    The large opening accepts the hanger head. The target then drops
    into the narrow slot so the shaft carries the target.

    These dimensions are physical hardware dimensions and must never
    be scaled with the target.
    """
    entry_center_y = slot_length / 2

    entry = Part.makeCylinder(
        entry_diameter / 2,
        thickness + 0.2,
        App.Vector(
            0,
            entry_center_y,
            z_offset - 0.1,
        ),
    )

    slot = Part.makeBox(
        slot_width,
        slot_length,
        thickness + 0.2,
        App.Vector(
            -slot_width / 2,
            -slot_length / 2,
            z_offset - 0.1,
        ),
    )

    return entry.fuse(
        slot
    ).removeSplitter()


def make_hanger_reinforcement(
    diameter=HANGER_REINFORCEMENT_DIAMETER,
    thickness=HANGER_REINFORCEMENT_THICKNESS,
    z_offset=HANGER_TEST_COUPON_THICKNESS,
):
    """
    Create a fixed-size reinforcement pad for the back of the target.
    """
    return Part.makeCylinder(
        diameter / 2,
        thickness,
        App.Vector(
            0,
            0,
            z_offset,
        ),
    )


def make_hanger_target_coupon(
    entry_diameter=HANGER_ENTRY_DIAMETER,
    slot_width=HANGER_SLOT_WIDTH,
    slot_length=HANGER_SLOT_LENGTH,
    reinforcement_diameter=HANGER_REINFORCEMENT_DIAMETER,
    reinforcement_thickness=HANGER_REINFORCEMENT_THICKNESS,
):
    """
    Create a small target-like coupon for testing the hanger interface.

    The visible target face remains flat at Z=0. Reinforcement is added
    only to the back.
    """
    coupon = Part.makeBox(
        HANGER_TEST_COUPON_WIDTH,
        HANGER_TEST_COUPON_HEIGHT,
        HANGER_TEST_COUPON_THICKNESS,
        App.Vector(
            -HANGER_TEST_COUPON_WIDTH / 2,
            -HANGER_TEST_COUPON_HEIGHT / 2,
            0,
        ),
    )

    reinforcement = make_hanger_reinforcement(
        diameter=reinforcement_diameter,
        thickness=reinforcement_thickness,
        z_offset=HANGER_TEST_COUPON_THICKNESS,
    )

    coupon = coupon.fuse(
        reinforcement
    ).removeSplitter()

    keyhole = make_hanger_keyhole_cut(
        entry_diameter=entry_diameter,
        slot_width=slot_width,
        slot_length=slot_length,
        thickness=(
            HANGER_TEST_COUPON_THICKNESS
            + reinforcement_thickness
        ),
    )

    return coupon.cut(
        keyhole
    ).removeSplitter()


def make_pvc_hanger_socket(
    pvc_od=PVC_HALF_INCH_OD,
    socket_diametral_clearance=HANGER_SOCKET_DIAMETRAL_CLEARANCE,
    socket_outer_diameter=HANGER_SOCKET_OUTER_DIAMETER,
    socket_height=HANGER_SOCKET_HEIGHT,
    socket_depth=HANGER_SOCKET_DEPTH,
    socket_lead_in_height=HANGER_SOCKET_LEAD_IN_HEIGHT,
    socket_lead_in_clearance=HANGER_SOCKET_LEAD_IN_CLEARANCE,
    boss_width=HANGER_BOSS_WIDTH,
    boss_height=HANGER_BOSS_HEIGHT,
    boss_projection=HANGER_BOSS_PROJECTION,
    boss_embed_depth=HANGER_BOSS_EMBED_DEPTH,
    peg_center_height=HANGER_PEG_CENTER_HEIGHT,
    peg_root_diameter=HANGER_PEG_ROOT_DIAMETER,
    peg_root_length=HANGER_PEG_ROOT_LENGTH,
    peg_taper_length=HANGER_PEG_TAPER_LENGTH,
    peg_shaft_diameter=HANGER_PEG_SHAFT_DIAMETER,
    peg_shaft_length=HANGER_PEG_SHAFT_LENGTH,
    peg_head_diameter=HANGER_PEG_HEAD_DIAMETER,
    peg_head_thickness=HANGER_PEG_HEAD_THICKNESS,
):
    """
    Create the reusable PVC-mounted target hanger.

    The outer body is built as a solid socket cylinder with a simple
    rectangular boss projecting from its side. The boss intersects the
    cylinder directly so the finished part reads as one continuous
    cylinder-plus-tab shape.

    After the outer body is fused, the PVC socket bore is cut into it.
    The male mushroom peg then projects from the outer face of the boss.

    All hanger-interface dimensions are physical dimensions and do
    not scale with the target.
    """
    socket_radius = socket_outer_diameter / 2

    pvc_socket_radius = (
        pvc_od
        + socket_diametral_clearance
    ) / 2

    if pvc_socket_radius >= socket_radius:
        raise ValueError(
            "PVC socket must be smaller than the hanger body."
        )

    if socket_depth >= socket_height:
        raise ValueError(
            "Socket depth must leave material at the top."
        )

    if boss_embed_depth <= 0:
        raise ValueError(
            "Boss embed depth must be greater than zero."
        )

    if boss_embed_depth >= (
        socket_radius - pvc_socket_radius
    ):
        raise ValueError(
            "Boss embed depth would break into the PVC socket bore."
        )

    if peg_shaft_diameter >= peg_root_diameter:
        raise ValueError(
            "Peg root diameter must be larger than shaft diameter."
        )

    if peg_head_diameter <= peg_shaft_diameter:
        raise ValueError(
            "Peg head diameter must be larger than shaft diameter."
        )

    # Build the OUTER body first: solid cylinder + rectangular boss.
    body = Part.makeCylinder(
        socket_radius,
        socket_height,
        App.Vector(
            0,
            0,
            0,
        ),
    )

    boss_start_x = (
        socket_radius
        - boss_embed_depth
    )

    boss_start_z = (
        peg_center_height
        - boss_height / 2
    )

    boss_depth = (
        boss_embed_depth
        + boss_projection
    )

    boss = Part.makeBox(
        boss_depth,
        boss_width,
        boss_height,
        App.Vector(
            boss_start_x,
            -boss_width / 2,
            boss_start_z,
        ),
    )

    body = body.fuse(
        boss
    ).removeSplitter()

    # Cut the PVC socket after the outer cylinder and boss are fused.
    bore = Part.makeCylinder(
        pvc_socket_radius,
        socket_depth + 0.1,
        App.Vector(
            0,
            0,
            -0.1,
        ),
    )

    if socket_lead_in_height > 0:
        lead_in = Part.makeCone(
            pvc_socket_radius
            + socket_lead_in_clearance,
            pvc_socket_radius,
            socket_lead_in_height + 0.1,
            App.Vector(
                0,
                0,
                -0.1,
            ),
            App.Vector(
                0,
                0,
                1,
            ),
        )

        bore = bore.fuse(
            lead_in
        ).removeSplitter()

    body = body.cut(
        bore
    ).removeSplitter()

    # Add the male hanger stud to the flat outer face of the boss.
    boss_outer_x = (
        socket_radius
        + boss_projection
    )

    peg_start_x = (
        boss_outer_x
        - 0.2
    )

    root = Part.makeCylinder(
        peg_root_diameter / 2,
        peg_root_length,
        App.Vector(
            peg_start_x,
            0,
            peg_center_height,
        ),
        App.Vector(
            1,
            0,
            0,
        ),
    )

    taper_start_x = (
        peg_start_x
        + peg_root_length
    )

    taper = Part.makeCone(
        peg_root_diameter / 2,
        peg_shaft_diameter / 2,
        peg_taper_length,
        App.Vector(
            taper_start_x,
            0,
            peg_center_height,
        ),
        App.Vector(
            1,
            0,
            0,
        ),
    )

    shaft_start_x = (
        taper_start_x
        + peg_taper_length
    )

    shaft = Part.makeCylinder(
        peg_shaft_diameter / 2,
        peg_shaft_length,
        App.Vector(
            shaft_start_x,
            0,
            peg_center_height,
        ),
        App.Vector(
            1,
            0,
            0,
        ),
    )

    head_start_x = (
        shaft_start_x
        + peg_shaft_length
    )

    head = Part.makeCylinder(
        peg_head_diameter / 2,
        peg_head_thickness,
        App.Vector(
            head_start_x,
            0,
            peg_center_height,
        ),
        App.Vector(
            1,
            0,
            0,
        ),
    )

    peg = root.fuse(
        taper
    )

    peg = peg.fuse(
        shaft
    )

    peg = peg.fuse(
        head
    ).removeSplitter()

    body = body.fuse(
        peg
    ).removeSplitter()

    return body

def create_pvc_hanger_test():
    """
    Create the actual reusable PVC hanger as a standalone test object.
    """
    document = App.newDocument(
        "PVC_Target_Hanger_Test"
    )

    hanger = document.addObject(
        "Part::Feature",
        "PVC_Target_Hanger",
    )

    hanger.Label = (
        '1/2" PVC Quick-Change Target Hanger'
    )

    hanger.Shape = make_pvc_hanger_socket()

    hanger.addProperty(
        "App::PropertyLength",
        "PVCOutsideDiameter",
        "Hanger",
    )

    hanger.addProperty(
        "App::PropertyLength",
        "SocketDiametralClearance",
        "Hanger",
    )

    hanger.addProperty(
        "App::PropertyLength",
        "PegHeadDiameter",
        "Hanger",
    )

    hanger.addProperty(
        "App::PropertyLength",
        "PegShaftDiameter",
        "Hanger",
    )

    hanger.PVCOutsideDiameter = (
        PVC_HALF_INCH_OD
    )

    hanger.SocketDiametralClearance = (
        HANGER_SOCKET_DIAMETRAL_CLEARANCE
    )

    hanger.PegHeadDiameter = (
        HANGER_PEG_HEAD_DIAMETER
    )

    hanger.PegShaftDiameter = (
        HANGER_PEG_SHAFT_DIAMETER
    )

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewAxonometric()
    view.fitAll()

    return hanger


def create_hanger_interface_test():
    """
    Create both sides of the quick-change hanger interface.

    The document contains:
      1. A reinforced target-side keyhole coupon.
      2. The actual PVC socket hanger with projecting male peg.
    """
    document = App.newDocument(
        "Target_Hanger_Interface_Test"
    )

    coupon = document.addObject(
        "Part::Feature",
        "Hanger_Keyhole_Test",
    )

    coupon.Label = (
        "Target Hanger Keyhole Test"
    )

    coupon.Shape = (
        make_hanger_target_coupon()
    )

    hanger_shape = (
        make_pvc_hanger_socket()
    )

    hanger_shape.translate(
        App.Vector(
            HANGER_TEST_OBJECT_SPACING,
            0,
            0,
        )
    )

    hanger = document.addObject(
        "Part::Feature",
        "PVC_Target_Hanger_Test",
    )

    hanger.Label = (
        '1/2" PVC Target Hanger Test'
    )

    hanger.Shape = hanger_shape

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewAxonometric()
    view.fitAll()

    return (
        coupon,
        hanger,
    )
