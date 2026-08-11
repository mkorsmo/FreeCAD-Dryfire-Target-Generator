import importlib

import FreeCAD as App


class ReloadDryFireTargetCommand:
    def GetResources(self):
        return {
            "MenuText": "Reload Dry Fire Targets",
            "ToolTip": "Reload Dry Fire Targets Python modules",
        }

    def Activated(self):
        from freecad_dryfire_target import dialog
        from freecad_dryfire_target import geometry

        from freecad_dryfire_target.uspsa import commands
        from freecad_dryfire_target.uspsa import dimensions
        from freecad_dryfire_target.uspsa import hardcover
        from freecad_dryfire_target.uspsa import target

        importlib.reload(geometry)
        importlib.reload(dialog)

        importlib.reload(dimensions)
        importlib.reload(target)
        importlib.reload(hardcover)
        importlib.reload(commands)

        App.Console.PrintMessage(
            "Dry Fire Targets modules reloaded.\n"
        )

    def IsActive(self):
        return True