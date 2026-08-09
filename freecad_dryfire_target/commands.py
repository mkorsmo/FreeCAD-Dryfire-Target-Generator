import importlib

import FreeCAD as App


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