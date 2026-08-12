import FreeCAD as App
import FreeCADGui as Gui
import Part


PVC_HALF_INCH_OD = 21.34

DEFAULT_SOCKET_DIAMETRAL_CLEARANCE = 0.30

DEFAULT_BASE_DIAMETER = 120.0
DEFAULT_BASE_TOP_DIAMETER = 112.0
DEFAULT_BASE_THICKNESS = 8.0

DEFAULT_BOSS_OUTER_DIAMETER = 38.0
DEFAULT_BOSS_HEIGHT = 32.0

DEFAULT_COLLAR_BOTTOM_DIAMETER = 52.0
DEFAULT_COLLAR_TOP_DIAMETER = DEFAULT_BOSS_OUTER_DIAMETER
DEFAULT_COLLAR_HEIGHT = 8.0

DEFAULT_SOCKET_DEPTH = 30.0
DEFAULT_SOCKET_FLOOR_THICKNESS = 2.0

DEFAULT_LEAD_IN_HEIGHT = 2.0
DEFAULT_LEAD_IN_RADIAL_CLEARANCE = 1.0

DEFAULT_TEST_BASE_DIAMETER = 48.0
DEFAULT_TEST_BASE_THICKNESS = 6.0


def make_base_body(
    base_diameter,
    base_top_diameter,
    base_thickness,
):
    base_radius = base_diameter / 2
    base_top_radius = base_top_diameter / 2

    if abs(base_radius - base_top_radius) < 0.0001:
        return Part.makeCylinder(
            base_radius,
            base_thickness,
            App.Vector(0, 0, 0),
        )

    return Part.makeCone(
        base_radius,
        base_top_radius,
        base_thickness,
        App.Vector(0, 0, 0),
        App.Vector(0, 0, 1),
    )


def make_socket_boss(
    base_thickness,
    boss_outer_diameter,
    boss_height,
    collar_bottom_diameter,
    collar_top_diameter,
    collar_height,
):
    boss = Part.makeCylinder(
        boss_outer_diameter / 2,
        boss_height,
        App.Vector(
            0,
            0,
            base_thickness,
        ),
    )

    if collar_height <= 0:
        return boss

    collar = Part.makeCone(
        collar_bottom_diameter / 2,
        collar_top_diameter / 2,
        collar_height,
        App.Vector(
            0,
            0,
            base_thickness,
        ),
        App.Vector(
            0,
            0,
            1,
        ),
    )

    return boss.fuse(
        collar
    ).removeSplitter()


def make_socket_cut(
    pvc_od,
    socket_diametral_clearance,
    base_thickness,
    boss_height,
    socket_depth,
    lead_in_height,
    lead_in_radial_clearance,
):
    total_height = (
        base_thickness
        + boss_height
    )

    socket_radius = (
        pvc_od
        + socket_diametral_clearance
    ) / 2

    socket_bottom_z = (
        total_height
        - socket_depth
    )

    socket = Part.makeCylinder(
        socket_radius,
        socket_depth + 0.1,
        App.Vector(
            0,
            0,
            socket_bottom_z,
        ),
    )

    if lead_in_height <= 0:
        return socket

    lead_in_bottom_z = (
        total_height
        - lead_in_height
    )

    lead_in = Part.makeCone(
        socket_radius,
        socket_radius
        + lead_in_radial_clearance,
        lead_in_height + 0.1,
        App.Vector(
            0,
            0,
            lead_in_bottom_z,
        ),
        App.Vector(
            0,
            0,
            1,
        ),
    )

    return socket.fuse(
        lead_in
    ).removeSplitter()


def make_tabletop_pvc_base(
    pvc_od=PVC_HALF_INCH_OD,
    socket_diametral_clearance=DEFAULT_SOCKET_DIAMETRAL_CLEARANCE,
    base_diameter=DEFAULT_BASE_DIAMETER,
    base_top_diameter=DEFAULT_BASE_TOP_DIAMETER,
    base_thickness=DEFAULT_BASE_THICKNESS,
    boss_outer_diameter=DEFAULT_BOSS_OUTER_DIAMETER,
    boss_height=DEFAULT_BOSS_HEIGHT,
    collar_bottom_diameter=DEFAULT_COLLAR_BOTTOM_DIAMETER,
    collar_top_diameter=DEFAULT_COLLAR_TOP_DIAMETER,
    collar_height=DEFAULT_COLLAR_HEIGHT,
    socket_depth=DEFAULT_SOCKET_DEPTH,
    socket_floor_thickness=DEFAULT_SOCKET_FLOOR_THICKNESS,
    lead_in_height=DEFAULT_LEAD_IN_HEIGHT,
    lead_in_radial_clearance=DEFAULT_LEAD_IN_RADIAL_CLEARANCE,
):
    """
    Create a freestanding tabletop base for nominal 1/2-inch PVC.

    The base prints flat on the build plate. A reinforced vertical
    socket rises from the center and accepts a short section of PVC.

    The default 0.30 mm diametral clearance is based on the tested
    socket coupon.
    """
    if base_diameter <= 0:
        raise ValueError(
            "Base diameter must be greater than zero."
        )

    if base_top_diameter <= 0:
        raise ValueError(
            "Base top diameter must be greater than zero."
        )

    if base_top_diameter > base_diameter:
        raise ValueError(
            "Base top diameter cannot exceed base diameter."
        )

    if base_thickness <= 0:
        raise ValueError(
            "Base thickness must be greater than zero."
        )

    if boss_outer_diameter <= 0:
        raise ValueError(
            "Boss outer diameter must be greater than zero."
        )

    if boss_height <= 0:
        raise ValueError(
            "Boss height must be greater than zero."
        )

    if collar_height < 0:
        raise ValueError(
            "Collar height cannot be negative."
        )

    if collar_bottom_diameter < boss_outer_diameter:
        raise ValueError(
            "Collar bottom diameter cannot be smaller than the boss."
        )

    if collar_top_diameter < boss_outer_diameter:
        raise ValueError(
            "Collar top diameter cannot be smaller than the boss."
        )

    if socket_depth <= 0:
        raise ValueError(
            "Socket depth must be greater than zero."
        )

    if socket_floor_thickness <= 0:
        raise ValueError(
            "Socket floor thickness must be greater than zero."
        )

    total_height = (
        base_thickness
        + boss_height
    )

    maximum_socket_depth = (
        total_height
        - socket_floor_thickness
    )

    if socket_depth > maximum_socket_depth:
        raise ValueError(
            "Socket depth leaves less than the requested floor thickness."
        )

    socket_diameter = (
        pvc_od
        + socket_diametral_clearance
    )

    if socket_diameter >= boss_outer_diameter:
        raise ValueError(
            "Socket diameter must be smaller than boss outer diameter."
        )

    base = make_base_body(
        base_diameter,
        base_top_diameter,
        base_thickness,
    )

    boss = make_socket_boss(
        base_thickness,
        boss_outer_diameter,
        boss_height,
        collar_bottom_diameter,
        collar_top_diameter,
        collar_height,
    )

    stand = base.fuse(
        boss
    ).removeSplitter()

    socket = make_socket_cut(
        pvc_od,
        socket_diametral_clearance,
        base_thickness,
        boss_height,
        socket_depth,
        lead_in_height,
        lead_in_radial_clearance,
    )

    stand = stand.cut(
        socket
    ).removeSplitter()

    return stand


def add_stand_properties(
    stand,
    pvc_od,
    socket_diametral_clearance,
    base_diameter,
    base_thickness,
    boss_outer_diameter,
    boss_height,
    socket_depth,
):
    stand.addProperty(
        "App::PropertyLength",
        "PVCOutsideDiameter",
        "PVC Stand",
    )

    stand.addProperty(
        "App::PropertyLength",
        "SocketDiametralClearance",
        "PVC Stand",
    )

    stand.addProperty(
        "App::PropertyLength",
        "BaseDiameter",
        "PVC Stand",
    )

    stand.addProperty(
        "App::PropertyLength",
        "BaseThickness",
        "PVC Stand",
    )

    stand.addProperty(
        "App::PropertyLength",
        "BossOuterDiameter",
        "PVC Stand",
    )

    stand.addProperty(
        "App::PropertyLength",
        "BossHeight",
        "PVC Stand",
    )

    stand.addProperty(
        "App::PropertyLength",
        "SocketDepth",
        "PVC Stand",
    )

    stand.PVCOutsideDiameter = pvc_od
    stand.SocketDiametralClearance = (
        socket_diametral_clearance
    )
    stand.BaseDiameter = base_diameter
    stand.BaseThickness = base_thickness
    stand.BossOuterDiameter = (
        boss_outer_diameter
    )
    stand.BossHeight = boss_height
    stand.SocketDepth = socket_depth


def create_tabletop_pvc_base(
    pvc_od=PVC_HALF_INCH_OD,
    socket_diametral_clearance=DEFAULT_SOCKET_DIAMETRAL_CLEARANCE,
    base_diameter=DEFAULT_BASE_DIAMETER,
    base_top_diameter=DEFAULT_BASE_TOP_DIAMETER,
    base_thickness=DEFAULT_BASE_THICKNESS,
    boss_outer_diameter=DEFAULT_BOSS_OUTER_DIAMETER,
    boss_height=DEFAULT_BOSS_HEIGHT,
    collar_bottom_diameter=DEFAULT_COLLAR_BOTTOM_DIAMETER,
    collar_top_diameter=DEFAULT_COLLAR_TOP_DIAMETER,
    collar_height=DEFAULT_COLLAR_HEIGHT,
    socket_depth=DEFAULT_SOCKET_DEPTH,
):
    """
    Create the full tabletop PVC target stand in a new document.
    """
    document = App.newDocument(
        "Tabletop_PVC_Target_Stand"
    )

    stand_shape = make_tabletop_pvc_base(
        pvc_od=pvc_od,
        socket_diametral_clearance=socket_diametral_clearance,
        base_diameter=base_diameter,
        base_top_diameter=base_top_diameter,
        base_thickness=base_thickness,
        boss_outer_diameter=boss_outer_diameter,
        boss_height=boss_height,
        collar_bottom_diameter=collar_bottom_diameter,
        collar_top_diameter=collar_top_diameter,
        collar_height=collar_height,
        socket_depth=socket_depth,
    )

    stand = document.addObject(
        "Part::Feature",
        "Tabletop_PVC_Target_Stand",
    )

    stand.Label = (
        'Tabletop Target Stand - 1/2" PVC'
    )

    stand.Shape = stand_shape

    add_stand_properties(
        stand,
        pvc_od,
        socket_diametral_clearance,
        base_diameter,
        base_thickness,
        boss_outer_diameter,
        boss_height,
        socket_depth,
    )

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewAxonometric()
    view.fitAll()

    return stand


def create_tabletop_pvc_socket_test(
    pvc_od=PVC_HALF_INCH_OD,
    socket_diametral_clearance=DEFAULT_SOCKET_DIAMETRAL_CLEARANCE,
):
    """
    Create a small socket-fit coupon using the same socket and boss
    geometry as the full stand.
    """
    document = App.newDocument(
        "Tabletop_PVC_Socket_Test"
    )

    test_shape = make_tabletop_pvc_base(
        pvc_od=pvc_od,
        socket_diametral_clearance=socket_diametral_clearance,
        base_diameter=DEFAULT_TEST_BASE_DIAMETER,
        base_top_diameter=DEFAULT_TEST_BASE_DIAMETER,
        base_thickness=DEFAULT_TEST_BASE_THICKNESS,
        boss_outer_diameter=DEFAULT_BOSS_OUTER_DIAMETER,
        boss_height=DEFAULT_BOSS_HEIGHT,
        collar_bottom_diameter=DEFAULT_BOSS_OUTER_DIAMETER,
        collar_top_diameter=DEFAULT_BOSS_OUTER_DIAMETER,
        collar_height=0.0,
        socket_depth=DEFAULT_SOCKET_DEPTH,
    )

    test = document.addObject(
        "Part::Feature",
        "Tabletop_PVC_Socket_Test",
    )

    test.Label = (
        'Tabletop Stand 1/2" PVC Socket Test'
    )

    test.Shape = test_shape

    test.addProperty(
        "App::PropertyLength",
        "PVCOutsideDiameter",
        "PVC Stand",
    )

    test.addProperty(
        "App::PropertyLength",
        "SocketDiametralClearance",
        "PVC Stand",
    )git

    test.PVCOutsideDiameter = pvc_od
    test.SocketDiametralClearance = (
        socket_diametral_clearance
    )

    document.recompute()

    view = Gui.activeDocument().activeView()
    view.viewAxonometric()
    view.fitAll()

    return test