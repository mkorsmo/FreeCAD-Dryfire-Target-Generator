import FreeCADGui as Gui

from freecad_dryfire_target.commands import (
    ReloadDryFireTargetCommand,
)

from freecad_dryfire_target.uspsa.commands import (
    CreateUSPSABodyHardCoverCommand,
    CreateUSPSACenterStripeCommand,
    CreateUSPSADiagonalLeftCommand,
    CreateUSPSADiagonalRightCommand,
    CreateUSPSALeftHalfCommand,
    CreateUSPSALowerHalfHardCoverCommand,
    CreateUSPSARightHalfCommand,
    CreateUSPSATargetCommand,
    CreateUSPSATuxedoCommand,
)


class DryFireTargetWorkbench(Workbench):
    MenuText = "Dry Fire Targets"
    ToolTip = "Generate scaled dry fire targets"

    def Initialize(self):
        Gui.addCommand(
            "DryFireTarget_USPSACardboard",
            CreateUSPSATargetCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSABodyHardCover",
            CreateUSPSABodyHardCoverCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSADiagonalRight",
            CreateUSPSADiagonalRightCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSADiagonalLeft",
            CreateUSPSADiagonalLeftCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSATuxedo",
            CreateUSPSATuxedoCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSALowerHalfHardCover",
            CreateUSPSALowerHalfHardCoverCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSARightHalf",
            CreateUSPSARightHalfCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSALeftHalf",
            CreateUSPSALeftHalfCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSACenterStripe",
            CreateUSPSACenterStripeCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_Reload",
            ReloadDryFireTargetCommand(),
        )

        commands = [
            "DryFireTarget_USPSACardboard",
            "DryFireTarget_USPSABodyHardCover",
            "DryFireTarget_USPSADiagonalRight",
            "DryFireTarget_USPSADiagonalLeft",
            "DryFireTarget_USPSATuxedo",
            "DryFireTarget_USPSALowerHalfHardCover",
            "DryFireTarget_USPSARightHalf",
            "DryFireTarget_USPSALeftHalf",
            "DryFireTarget_USPSACenterStripe",
            "Separator",
            "DryFireTarget_Reload",
        ]

        self.appendToolbar(
            "Dry Fire Targets",
            commands,
        )

        self.appendMenu(
            "Dry Fire Targets",
            commands,
        )

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(DryFireTargetWorkbench())