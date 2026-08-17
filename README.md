# FreeCAD Dry Fire Target Generator

A FreeCAD workbench for generating parametric, 3D-printable dry-fire targets.

The project started as a way to replace fixed PDF/image-based dry-fire targets with actual CAD geometry. Targets can be generated at common reduced scales, custom scales, or sized to simulate a greater shooting distance while keeping the target at a practical indoor distance.

Current support includes USPSA cardboard targets, IPSC Classic cardboard targets, common hard-cover patterns, and several steel target shapes.

## Features

- Native FreeCAD workbench: **Dry Fire Targets**
- Parametric USPSA cardboard target geometry
- Parametric IPSC Classic cardboard target geometry
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
- USPSA hard-cover target patterns
- IPSC Classic hard-cover target patterns
- Face-down multipart construction for hard-cover targets
- Steel target generator
- Optional vertical 1/2-inch PVC snap-clip mounts for cardboard targets
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

All USPSA cardboard target types are selected from a single **Create USPSA Target** dialog.

The full-size USPSA target geometry is defined as 450 × 750 mm.

Common generated sizes are:

| Scale | Approximate Size |
| --- | --- |
| 1/2 | 225 × 375 mm |
| 1/3 | 150 × 250 mm |
| 1/4 | 112.5 × 187.5 mm |

## IPSC Classic Target Types

The IPSC generator currently includes:

| Target | Description |
| --- | --- |
| Standard IPSC | Standard IPSC Classic cardboard target with A, C, and D scoring grooves |
| Classic Hardcover V2 | Diagonal right hard cover |
| Classic Hardcover V3 | Diagonal left hard cover |

The full-size IPSC Classic target geometry is defined as 450 × 570 mm and includes the 5 mm non-scoring border.

All IPSC target types are selected from a single **Create IPSC Target** dialog.

Additional IPSC Classic hard-cover variants are planned.

## Steel Targets

The steel generator currently includes:

### Round Plates

- 8-inch round plate
- 10-inch round plate
- 12-inch round plate

### Square Plates

- 6-inch square plate
- 8-inch square plate
- 10-inch square plate
- 12-inch square plate

### Poppers

- USPSA Popper
- USPSA Mini-Popper

The popper silhouettes are generated from dimensional target geometry rather than approximated image tracing.

Steel targets use the same scale options as the cardboard generators and are created from the **Create Steel Target** dialog.

## Scaling

The generators can create targets using preset scales or a calculated simulated-distance scale.

### Simulated Distance

Scale is calculated as:

```text
scale = actual distance / simulated distance
```

For example, placing a target at 10 feet and asking it to represent a target at 30 feet produces:

```text
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

Scoring grooves are cut only into the exposed cardboard areas. Scoring lines underneath hard cover are therefore not printed into the visible hard-cover surface.

The cardboard and hard-cover face layers are placed at the build-plate side of the model, with the structural back above them. This makes it possible to assign separate materials or colors in the slicer while keeping the target aligned as one multipart object.

When exporting a hard-cover target, keep the generated parts aligned and import them into the slicer together as parts of the same object.

## Mounts

USPSA and IPSC cardboard targets can optionally include a back-mounted snap clip for nominal 1/2-inch PVC.

The mount geometry is kept at physical size regardless of target scale. Only the mount positions are scaled with the target.

The current mount option is:

```text
Vertical 1/2" PVC
```

Targets with mounts are generated with the scoring face oriented appropriately and the clip geometry fused to the back of the target.

Hard-cover targets keep the face layers separate while the mount is fused into the structural back.

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
3. Choose one of:
   - **Create USPSA Target**
   - **Create IPSC Target**
   - **Create Steel Target**
4. Select the desired target type.
5. Choose a scale preset, custom scale, or simulated-distance mode.
6. Adjust print geometry if needed.
7. Select a mount option when available.
8. Click **OK** to generate the target.

The default cardboard target settings are:

```text
Scale:         1/3
Thickness:     1.2 mm
Groove width:  0.6 mm
Groove depth:  0.3 mm
```

## Printing

The generated geometry is intended for normal FDM printing.

Standard cardboard and steel targets are generated as single parts.

Hard-cover targets are specifically constructed for **face-down printing**. The cardboard and hard-cover face geometry is placed against the build plate, with the structural backing above it.

Mounted targets include the mount geometry on the back of the target.

Because printer tolerances, first-layer behavior, filament, and slicer settings vary, inspect the sliced model before printing.

## Project Structure

```text
FreeCAD-Dryfire-Target-Generator/
├── freecad_dryfire_target/
│   ├── commands.py
│   ├── dialog.py
│   ├── geometry.py
│   ├── mounts.py
│   ├── stands.py
│   ├── __init__.py
│   ├── ipsc/
│   │   ├── commands.py
│   │   ├── dimensions.py
│   │   ├── hardcover.py
│   │   ├── __init__.py
│   │   └── target.py
│   ├── steel/
│   │   ├── commands.py
│   │   ├── dimensions.py
│   │   ├── __init__.py
│   │   └── target.py
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

The code is intentionally split so that generic workbench, UI, mount, and geometry functionality stays separate from target-family-specific geometry.

- `geometry.py` contains reusable geometry helpers.
- `dialog.py` contains the generic cardboard target settings dialog.
- `mounts.py` contains reusable target-mount geometry.
- `stands.py` contains reusable target-stand geometry.
- `uspsa/` contains USPSA cardboard target geometry, hard-cover masks, and commands.
- `ipsc/` contains IPSC Classic cardboard target geometry, hard-cover masks, and commands.
- `steel/` contains steel plate and popper geometry and commands.

This structure is intended to make additional target families easier to add without turning any one implementation into a large monolithic module.

## Development

The project is actively evolving.

Current areas of development include:

- additional IPSC Classic hard-cover variants
- additional target families
- mounting and quick-change systems
- reusable stands
- slicer-friendly export workflows

The **Reload Dry Fire Targets** command reloads the Python modules used by the workbench, which is useful while editing target geometry.

Changes to `InitGui.py` generally require restarting FreeCAD.

## Safety

These are dry-fire training aids only.

Follow normal firearm-safety practices during dry-fire training, including maintaining a safe direction and keeping live ammunition out of the training area.

## License

This project is released under the [MIT License](LICENSE).

Copyright © 2026 Matthew Korsmo.

## Disclaimer

This is an independent project and is not affiliated with or endorsed by USPSA or IPSC.
