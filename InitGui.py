import FreeCADGui as Gui


class DryFireTargetWorkbench(Workbench):
    MenuText = "Dry Fire Targets"
    ToolTip = "Generate scaled dry fire targets"

    def Initialize(self):
        from freecad_dryfire_target import uspsa
        from freecad_dryfire_target.commands import (
            ReloadDryFireTargetCommand,
        )

        Gui.addCommand(
            "DryFireTarget_USPSACardboard",
            uspsa.CreateUSPSATargetCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_USPSACenterStripe",
            uspsa.CreateUSPSACenterStripeCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_Reload",
            ReloadDryFireTargetCommand(),
        )

        commands = [
            "DryFireTarget_USPSACardboard",
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