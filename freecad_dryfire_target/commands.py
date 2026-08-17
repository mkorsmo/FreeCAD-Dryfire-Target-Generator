import importlib

import FreeCAD as App


class ReloadDryFireTargetCommand:
    def GetResources(self):
        return {
            "MenuText": "Reload",
            "ToolTip": (
                "Reload Dry Fire Targets "
                "Python modules"
            ),
        }

    def Activated(self):
        from freecad_dryfire_target import (
            dialog,
            geometry,
            mounts,
        )

        importlib.reload(
            geometry
        )
        importlib.reload(
            mounts
        )
        importlib.reload(
            dialog
        )

        try:
            from freecad_dryfire_target import (
                stands,
            )

            importlib.reload(
                stands
            )

        except ImportError:
            pass

        from freecad_dryfire_target.uspsa import (
            commands as uspsa_commands,
            dimensions as uspsa_dimensions,
            hardcover as uspsa_hardcover,
            target as uspsa_target,
        )

        importlib.reload(
            uspsa_dimensions
        )
        importlib.reload(
            uspsa_target
        )
        importlib.reload(
            uspsa_hardcover
        )
        importlib.reload(
            uspsa_commands
        )

        from freecad_dryfire_target.ipsc import (
            commands as ipsc_commands,
            dimensions as ipsc_dimensions,
            target as ipsc_target,
        )

        importlib.reload(
            ipsc_dimensions
        )
        importlib.reload(
            ipsc_target
        )
        importlib.reload(
            ipsc_commands
        )

        from freecad_dryfire_target.steel import (
            commands as steel_commands,
            dimensions as steel_dimensions,
            target as steel_target,
        )

        importlib.reload(
            steel_dimensions
        )
        importlib.reload(
            steel_target
        )
        importlib.reload(
            steel_commands
        )

        App.Console.PrintMessage(
            "Dry Fire Targets modules reloaded.\n"
        )

    def IsActive(self):
        return True
