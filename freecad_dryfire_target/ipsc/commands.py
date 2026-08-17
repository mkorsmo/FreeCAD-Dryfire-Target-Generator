import FreeCAD as App
import FreeCADGui as Gui

from freecad_dryfire_target.dialog import (
    TargetSettingsDialog,
)

from freecad_dryfire_target.ipsc.dimensions import (
    DEFAULT_GROOVE_DEPTH,
    DEFAULT_GROOVE_WIDTH,
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    TARGET_HEIGHT,
    TARGET_WIDTH,
)

from freecad_dryfire_target.ipsc.hardcover import (
    create_classic_2_target,
    create_classic_3_target,
)

from freecad_dryfire_target.ipsc.target import (
    MOUNT_NONE,
    MOUNT_VERTICAL_PVC,
    create_target,
)


TARGET_TYPES = [
    (
        "Standard IPSC",
        "standard",
    ),
    (
        "Classic Hardcover V2 - Diagonal Right",
        "classic_2",
    ),
    (
        "Classic Hardcover V3 - Diagonal Left",
        "classic_3",
    ),
]

MOUNT_TYPES = [
    (
        "None",
        MOUNT_NONE,
    ),
    (
        'Vertical 1/2" PVC',
        MOUNT_VERTICAL_PVC,
    ),
]

TARGET_CREATORS = {
    "standard": create_target,
    "classic_2": create_classic_2_target,
    "classic_3": create_classic_3_target,
}


def show_target_dialog():
    dialog = TargetSettingsDialog(
        title="IPSC Dry Fire Target",
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        target_types=TARGET_TYPES,
        mount_types=MOUNT_TYPES,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = (
        dialog.get_settings()
    )

    target_type = settings[
        "target_type"
    ]

    creator = TARGET_CREATORS.get(
        target_type
    )

    if creator is None:
        App.Console.PrintError(
            f"Unknown IPSC target type: {target_type}\n"
        )
        return

    if target_type != "standard":
        App.Console.PrintMessage(
            "Hard cover target uses face-down split parts.\n"
        )

    creator(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings[
            "groove_width"
        ],
        groove_depth=settings[
            "groove_depth"
        ],
        mount=settings["mount"],
    )


class CreateIPSCTargetCommand:
    def GetResources(self):
        return {
            "MenuText": (
                "Create IPSC Target"
            ),
            "ToolTip": (
                "Create a scaled IPSC "
                "dry fire target"
            ),
        }

    def Activated(self):
        show_target_dialog()

    def IsActive(self):
        return True
