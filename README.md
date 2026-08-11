# FreeCAD Dry Fire Target Generator

A FreeCAD workbench for generating parametric, 3D-printable dry-fire targets.

The project started as a way to replace fixed PDF/image-based dry-fire targets with actual CAD geometry. Targets can be generated at common reduced scales, custom scales, or sized to simulate a greater shooting distance while keeping the target at a practical indoor distance.

Current target support is focused on USPSA cardboard targets, including scoring zones and several common hard-cover configurations.

## Features

- Native FreeCAD workbench: **Dry Fire Targets**
- Parametric USPSA cardboard target geometry
- A, C, and D scoring-zone grooves
- Common scale presets:
  - 1/2 scale
  - 1/3 scale
  - 1/4 scale
- Custom target scale
- Simulated-distance scaling
- Adjustable:
  - target thickness
  - scoring-groove width
  - scoring-groove depth
- Multiple USPSA hard-cover patterns
- Face-down multipart construction for hard-cover targets
- Reload command for faster development without restarting FreeCAD for normal Python-module changes

## USPSA Target Types

The USPSA generator currently includes:

| Target | Description |
| --- | --- |
| Standard USPSA | Standard cardboard target with scoring grooves |
| Hard Cover V1 | Body hard cover |
| Hard Cover V2 | Diagonal right |
| Hard Cover V3 | Diagonal left |
| Hard Cover V4 | Tuxedo |
| Hard Cover V5 | Lower-half hard cover |
| Hard Cover V6 | Right-side half of the Tuxedo pattern |
| Hard Cover V7 | Left-side half of the Tuxedo pattern |
| Center Stripe | Centered 2-inch / 50.8 mm hard-cover stripe |

All target types are selected from a single **Create USPSA Target** dialog.

## Scaling

The full-size target geometry is defined as 450 × 750 mm.

Common generated sizes are:

| Scale | Approximate Size |
| --- | --- |
| 1/2 | 225 × 375 mm |
| 1/3 | 150 × 250 mm |
| 1/4 | 112.5 × 187.5 mm |

### Simulated Distance

The generator can also calculate scale based on an actual shooting distance and a desired simulated distance.

For example, placing a target at 10 feet and asking it to represent a target at 30 feet produces:

```text
scale = actual distance / simulated distance
scale = 10 / 30
scale = 1/3
```

This preserves the target's approximate angular size from the shooter's point of view.

## Hard-Cover Targets

Hard-cover targets use a multipart face-down design.

Instead of simply placing black geometry on top of a finished target, the generator creates aligned parts for:

- the structural target back
- the exposed cardboard face
- the hard-cover face

Scoring grooves are cut only into the exposed cardboard areas.

This lets the target print with the visible face against the build plate while preserving separate cardboard and hard-cover regions for slicer assignment.

When exporting a hard-cover target, keep the generated parts aligned and import them into the slicer together as parts of the same object.

## Installation

Clone the repository:

```bash
git clone https://github.com/mkorsmo/FreeCAD-Dryfire-Target-Generator.git
cd FreeCAD-Dryfire-Target-Generator
```

The repository itself is a FreeCAD workbench, so FreeCAD needs to see the repository root inside its user `Mod` directory.

On Linux, a symlink is convenient during development:

```bash
ln -s "$(pwd)" ~/.local/share/FreeCAD/Mod/FreeCADDryFireTarget
```

Some FreeCAD installations use a version-specific directory, for example:

```bash
~/.local/share/FreeCAD/v1-1/Mod
```

Adjust the path for your FreeCAD installation.

You can also copy the repository into the `Mod` directory instead of using a symlink.

Restart FreeCAD after initially installing the workbench or after changing `InitGui.py`.

## Usage

1. Start FreeCAD.
2. Select **Dry Fire Targets** from the workbench selector.
3. Click **Create USPSA Target**.
4. Select the desired target type.
5. Choose a scale preset, custom scale, or simulated-distance mode.
6. Adjust print geometry if needed.
7. Click **OK** to generate the target.

The default target settings are:

```text
Scale:         1/3
Thickness:     1.2 mm
Groove width:  0.6 mm
Groove depth:  0.3 mm
```

A 1/3-scale USPSA target is approximately 150 × 250 mm.

## Printing

The generated geometry is intended for normal FDM printing.

For standard targets, orient the scoring face as desired for your printer and preferred surface finish.

Hard-cover targets are specifically constructed for **face-down printing**. The cardboard and hard-cover face geometry is placed against the build plate, with the structural backing above it.

Because printer tolerances, first-layer behavior, filament, and slicer settings vary, inspect the sliced model before printing.

## Project Structure

```text
FreeCAD-Dryfire-Target-Generator/
├── freecad_dryfire_target/
│   ├── commands.py
│   ├── dialog.py
│   ├── geometry.py
│   ├── __init__.py
│   └── uspsa/
│       ├── commands.py
│       ├── dimensions.py
│       ├── hardcover.py
│       ├── __init__.py
│       └── target.py
├── InitGui.py
├── Init.py
├── LICENSE
└── README.md
```

The code is intentionally split so that generic workbench/UI/geometry functionality stays separate from USPSA-specific geometry.

- `geometry.py` contains reusable geometry helpers.
- `dialog.py` contains the generic target settings dialog.
- `uspsa/dimensions.py` contains USPSA dimensions and defaults.
- `uspsa/target.py` builds the standard target and scoring geometry.
- `uspsa/hardcover.py` contains hard-cover masks and multipart target construction.
- `uspsa/commands.py` connects USPSA target types to the FreeCAD UI.

This structure is intended to make additional target families easier to add without turning the USPSA implementation into one large module.

## Development

The project is actively evolving.

Current areas of experimentation include optional target mounting systems, including snap-on mounting for nominal 1/2-inch PVC.

Other target types and training-target features may be added over time.

The **Reload Dry Fire Targets** command reloads the Python modules used by the workbench, which is useful while editing target geometry. Changes to `InitGui.py` generally require restarting FreeCAD.

## Safety

These are dry-fire training aids only. Follow normal firearm-safety practices during dry-fire training, including maintaining a safe direction and keeping live ammunition out of the training area.

## License

This project is released under the [MIT License](LICENSE).

Copyright © 2026 Matthew Korsmo.

## Disclaimer

This is an independent project and is not affiliated with or endorsed by USPSA.
