import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.dialog import TargetSettingsDialog

from freecad_dryfire_target.uspsa.dimensions import (
    DEFAULT_GROOVE_DEPTH,
    DEFAULT_GROOVE_WIDTH,
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    TARGET_HEIGHT,
    TARGET_WIDTH,
)

from freecad_dryfire_target.uspsa.hardcover import (
    create_body_hard_cover_target,
    create_center_stripe_target,
    create_diagonal_left_target,
    create_diagonal_right_target,
    create_left_half_target,
    create_lower_half_hard_cover_target,
    create_right_half_target,
    create_tuxedo_target,
)

from freecad_dryfire_target.uspsa.target import (
    MOUNT_LAYOUT_BOTTOM,
    MOUNT_LAYOUT_MIDDLE,
    MOUNT_LAYOUT_TOP,
    MOUNT_LAYOUT_TOP_BOTTOM,
    MOUNT_NONE,
    MOUNT_VERTICAL_PVC,
    create_target,
)


TARGET_TYPES = [
    ("Standard USPSA", "standard"),
    ("Hard Cover V1 - Body", "body"),
    ("Hard Cover V2 - Diagonal Right", "diagonal_right"),
    ("Hard Cover V3 - Diagonal Left", "diagonal_left"),
    ("Hard Cover V4 - Tuxedo", "tuxedo"),
    ("Hard Cover V5 - Lower Half", "lower_half"),
    ("Hard Cover V6 - Right Side", "right_side"),
    ("Hard Cover V7 - Left Side", "left_side"),
    ("Center Stripe", "center_stripe"),
]


MOUNT_TYPES = [
    ("None", MOUNT_NONE),
    ('Vertical 1/2" PVC', MOUNT_VERTICAL_PVC),
]


MOUNT_LAYOUT_TYPES = [
    ("Top + Bottom", MOUNT_LAYOUT_TOP_BOTTOM),
    ("Top", MOUNT_LAYOUT_TOP),
    ("Middle", MOUNT_LAYOUT_MIDDLE),
    ("Bottom", MOUNT_LAYOUT_BOTTOM),
]


TARGET_CREATORS = {
    "standard": create_target,
    "body": create_body_hard_cover_target,
    "diagonal_right": create_diagonal_right_target,
    "diagonal_left": create_diagonal_left_target,
    "tuxedo": create_tuxedo_target,
    "lower_half": create_lower_half_hard_cover_target,
    "right_side": create_right_half_target,
    "left_side": create_left_half_target,
    "center_stripe": create_center_stripe_target,
}


def show_target_dialog():
    dialog = TargetSettingsDialog(
        title="USPSA Dry Fire Target",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        target_types=TARGET_TYPES,
        mount_types=MOUNT_TYPES,
        mount_layout_types=MOUNT_LAYOUT_TYPES,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()
    target_type = settings["target_type"]

    creator = TARGET_CREATORS.get(
        target_type
    )

    if creator is None:
        App.Console.PrintError(
            f"Unknown USPSA target type: {target_type}\n"
        )
        return

    if target_type != "standard":
        App.Console.PrintMessage(
            "Hard cover target uses face-down split parts.\n"
        )

    creator(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
        mount=settings["mount"],
        mount_layout=settings["mount_layout"],
    )


class CreateUSPSATargetCommand:
    def GetResources(self):
        return {
            "MenuText": "Create USPSA Target",
            "ToolTip": (
                "Create a scaled USPSA dry fire target"
            ),
        }

    def Activated(self):
        show_target_dialog()

    def IsActive(self):
        return True