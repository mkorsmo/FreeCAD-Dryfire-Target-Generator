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
    create_target,
)


def show_create_dialog(
    title,
    creator,
    message=None,
):
    dialog = TargetSettingsDialog(
        title=title,
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        default_scale=DEFAULT_SCALE,
        default_thickness=DEFAULT_THICKNESS,
        default_groove_width=DEFAULT_GROOVE_WIDTH,
        default_groove_depth=DEFAULT_GROOVE_DEPTH,
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    if message:
        App.Console.PrintMessage(
            f"{message}\n"
        )

    creator(
        scale=settings["scale"],
        thickness=settings["thickness"],
        groove_width=settings["groove_width"],
        groove_depth=settings["groove_depth"],
    )


def show_target_dialog():
    show_create_dialog(
        title="USPSA Cardboard Target",
        creator=create_target,
    )


def show_body_hard_cover_dialog():
    show_create_dialog(
        title="USPSA Body Hard Cover",
        creator=create_body_hard_cover_target,
        message=(
            "Body hard cover uses "
            "face-down split parts."
        ),
    )


def show_diagonal_right_dialog():
    show_create_dialog(
        title="USPSA Diagonal Right Hard Cover",
        creator=create_diagonal_right_target,
        message=(
            "Diagonal Right hard cover uses "
            "face-down split parts."
        ),
    )


def show_diagonal_left_dialog():
    show_create_dialog(
        title="USPSA Diagonal Left Hard Cover",
        creator=create_diagonal_left_target,
        message=(
            "Diagonal Left hard cover uses "
            "face-down split parts."
        ),
    )


def show_tuxedo_dialog():
    show_create_dialog(
        title="USPSA Tuxedo Hard Cover",
        creator=create_tuxedo_target,
        message=(
            "Tuxedo hard cover uses "
            "face-down split parts."
        ),
    )


def show_lower_half_hard_cover_dialog():
    show_create_dialog(
        title="USPSA Lower Half Hard Cover",
        creator=create_lower_half_hard_cover_target,
        message=(
            "Lower Half hard cover uses "
            "face-down split parts."
        ),
    )


def show_right_half_dialog():
    show_create_dialog(
        title="USPSA Right Half Hard Cover",
        creator=create_right_half_target,
        message=(
            "Right Half hard cover uses "
            "face-down split parts."
        ),
    )


def show_left_half_dialog():
    show_create_dialog(
        title="USPSA Left Half Hard Cover",
        creator=create_left_half_target,
        message=(
            "Left Half hard cover uses "
            "face-down split parts."
        ),
    )


def show_center_stripe_dialog():
    show_create_dialog(
        title="USPSA Center Stripe Hard Cover",
        creator=create_center_stripe_target,
        message=(
            "Center Stripe hard cover uses "
            "face-down split parts."
        ),
    )


class CreateUSPSATargetCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Cardboard Target",
            "ToolTip": (
                "Create a scaled USPSA "
                "cardboard dry fire target"
            ),
        }

    def Activated(self):
        show_target_dialog()

    def IsActive(self):
        return True


class CreateUSPSABodyHardCoverCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Body Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 1",
        }

    def Activated(self):
        show_body_hard_cover_dialog()

    def IsActive(self):
        return True


class CreateUSPSADiagonalRightCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Diagonal Right Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 2",
        }

    def Activated(self):
        show_diagonal_right_dialog()

    def IsActive(self):
        return True


class CreateUSPSADiagonalLeftCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Diagonal Left Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 3",
        }

    def Activated(self):
        show_diagonal_left_dialog()

    def IsActive(self):
        return True


class CreateUSPSATuxedoCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Tuxedo Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 4",
        }

    def Activated(self):
        show_tuxedo_dialog()

    def IsActive(self):
        return True


class CreateUSPSALowerHalfHardCoverCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Lower Half Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 5",
        }

    def Activated(self):
        show_lower_half_hard_cover_dialog()

    def IsActive(self):
        return True


class CreateUSPSARightHalfCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Right Half Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 6",
        }

    def Activated(self):
        show_right_half_dialog()

    def IsActive(self):
        return True


class CreateUSPSALeftHalfCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Left Half Hard Cover",
            "ToolTip": "Create USPSA Hardcover Version 7",
        }

    def Activated(self):
        show_left_half_dialog()

    def IsActive(self):
        return True


class CreateUSPSACenterStripeCommand:
    def GetResources(self):
        return {
            "MenuText": "USPSA Center Stripe Hard Cover",
            "ToolTip": (
                "Create a USPSA center stripe "
                "hard cover target"
            ),
        }

    def Activated(self):
        show_center_stripe_dialog()

    def IsActive(self):
        return True