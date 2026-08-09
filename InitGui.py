import importlib

import FreeCAD as App
import FreeCADGui as Gui


class ReloadDryFireTargetCommand:
    def GetResources(self):
        return {
            "MenuText": "Reload Dry Fire Targets",
            "ToolTip": "Reload the Dry Fire Targets plugin modules",
        }

    def Activated(self):
        from freecad_dryfire_target import dialog
        from freecad_dryfire_target import geometry
        from freecad_dryfire_target import uspsa

        importlib.reload(geometry)
        importlib.reload(dialog)
        importlib.reload(uspsa)

        App.Console.PrintMessage(
            "Dry Fire Targets modules reloaded.\n"
        )

    def IsActive(self):
        return True


class DryFireTargetWorkbench(Workbench):
    MenuText = "Dry Fire Targets"
    ToolTip = "Generate scaled dry fire targets"

    def Initialize(self):
        from freecad_dryfire_target import uspsa

        Gui.addCommand(
            "DryFireTarget_USPSACardboard",
            uspsa.CreateUSPSATargetCommand(),
        )

        Gui.addCommand(
            "DryFireTarget_Reload",
            ReloadDryFireTargetCommand(),
        )

        commands = [
            "DryFireTarget_USPSACardboard",
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