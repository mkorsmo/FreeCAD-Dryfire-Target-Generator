import FreeCADGui as Gui


class DryFireTargetWorkbench(Workbench):
    MenuText = "Dry Fire Targets"
    ToolTip = "Generate scaled dry fire targets"

    def Initialize(self):
        from freecad_dryfire_target import commands as core_commands
        from freecad_dryfire_target.uspsa import commands as uspsa_commands

        Gui.addCommand(
            "DryFireTarget_USPSATarget",
            uspsa_commands.CreateUSPSATargetCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_Reload",
            core_commands.ReloadDryFireTargetCommand(),
        )

        commands = [
            "DryFireTarget_USPSATarget",
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
