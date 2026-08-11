import FreeCADGui as Gui


class DryFireTargetWorkbench(Workbench):
    MenuText = "Dry Fire Targets"
    ToolTip = "Generate scaled dry fire targets"

    def Initialize(self):
        from freecad_dryfire_target import commands as core_commands
        from freecad_dryfire_target.uspsa import commands as uspsa_commands

        Gui.addCommand(
            "DryFireTarget_USPSACardboard",
            uspsa_commands.CreateUSPSATargetCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSABodyHardCover",
            uspsa_commands.CreateUSPSABodyHardCoverCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSADiagonalRight",
            uspsa_commands.CreateUSPSADiagonalRightCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSADiagonalLeft",
            uspsa_commands.CreateUSPSADiagonalLeftCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSATuxedo",
            uspsa_commands.CreateUSPSATuxedoCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSALowerHalfHardCover",
            uspsa_commands.CreateUSPSALowerHalfHardCoverCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSARightHalf",
            uspsa_commands.CreateUSPSARightHalfCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSALeftHalf",
            uspsa_commands.CreateUSPSALeftHalfCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSACenterStripe",
            uspsa_commands.CreateUSPSACenterStripeCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_Reload",
            core_commands.ReloadDryFireTargetCommand(),
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