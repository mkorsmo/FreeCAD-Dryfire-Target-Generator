import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtWidgets

from freecad_dryfire_target.steel.dimensions import (
    DEFAULT_SCALE,
    DEFAULT_THICKNESS,
    TARGET_TYPES,
)
from freecad_dryfire_target.steel.target import (
    create_steel_target,
)


class SteelTargetDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Steel Dry Fire Target"
        )
        self.setMinimumWidth(
            360
        )

        self.build_ui()
        self.select_scale(
            DEFAULT_SCALE
        )
        self.update_scale_controls()
        self.update_target_size()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(
            self
        )

        target_group = QtWidgets.QGroupBox(
            "Target"
        )
        target_layout = QtWidgets.QFormLayout(
            target_group
        )

        self.target_type_combo = (
            QtWidgets.QComboBox()
        )

        for target_type, target_info in TARGET_TYPES.items():
            self.target_type_combo.addItem(
                target_info["label"],
                target_type,
            )

        target_layout.addRow(
            "Target type:",
            self.target_type_combo,
        )

        layout.addWidget(
            target_group
        )

        scale_group = QtWidgets.QGroupBox(
            "Scale"
        )
        scale_layout = QtWidgets.QFormLayout(
            scale_group
        )

        self.scale_combo = QtWidgets.QComboBox()
        self.scale_combo.addItem(
            "1/2 scale",
            1 / 2,
        )
        self.scale_combo.addItem(
            "1/3 scale",
            1 / 3,
        )
        self.scale_combo.addItem(
            "1/4 scale",
            1 / 4,
        )
        self.scale_combo.addItem(
            "Custom",
            "custom",
        )
        self.scale_combo.addItem(
            "Simulated distance",
            "distance",
        )

        self.custom_scale = QtWidgets.QDoubleSpinBox()
        self.custom_scale.setDecimals(
            4
        )
        self.custom_scale.setRange(
            0.01,
            1.0,
        )
        self.custom_scale.setSingleStep(
            0.01
        )
        self.custom_scale.setValue(
            DEFAULT_SCALE
        )

        self.actual_distance = QtWidgets.QDoubleSpinBox()
        self.actual_distance.setDecimals(
            1
        )
        self.actual_distance.setRange(
            1.0,
            500.0,
        )
        self.actual_distance.setSuffix(
            " ft"
        )
        self.actual_distance.setValue(
            10.0
        )

        self.simulated_distance = QtWidgets.QDoubleSpinBox()
        self.simulated_distance.setDecimals(
            1
        )
        self.simulated_distance.setRange(
            1.0,
            500.0,
        )
        self.simulated_distance.setSuffix(
            " ft"
        )
        self.simulated_distance.setValue(
            30.0
        )

        self.calculated_scale_label = QtWidgets.QLabel()
        self.target_size_label = QtWidgets.QLabel()

        scale_layout.addRow(
            "Scale:",
            self.scale_combo,
        )
        scale_layout.addRow(
            "Custom:",
            self.custom_scale,
        )
        scale_layout.addRow(
            "Actual distance:",
            self.actual_distance,
        )
        scale_layout.addRow(
            "Simulated distance:",
            self.simulated_distance,
        )
        scale_layout.addRow(
            "Calculated scale:",
            self.calculated_scale_label,
        )
        scale_layout.addRow(
            "Target size:",
            self.target_size_label,
        )

        layout.addWidget(
            scale_group
        )

        print_group = QtWidgets.QGroupBox(
            "Print Geometry"
        )
        print_layout = QtWidgets.QFormLayout(
            print_group
        )

        self.thickness = QtWidgets.QDoubleSpinBox()
        self.thickness.setDecimals(
            2
        )
        self.thickness.setRange(
            0.2,
            10.0,
        )
        self.thickness.setSingleStep(
            0.1
        )
        self.thickness.setSuffix(
            " mm"
        )
        self.thickness.setValue(
            DEFAULT_THICKNESS
        )

        print_layout.addRow(
            "Thickness:",
            self.thickness,
        )

        layout.addWidget(
            print_group
        )

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )
        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

        self.target_type_combo.currentIndexChanged.connect(
            self.update_target_size
        )
        self.scale_combo.currentIndexChanged.connect(
            self.update_scale_controls
        )
        self.scale_combo.currentIndexChanged.connect(
            self.update_target_size
        )
        self.custom_scale.valueChanged.connect(
            self.update_target_size
        )
        self.actual_distance.valueChanged.connect(
            self.update_target_size
        )
        self.simulated_distance.valueChanged.connect(
            self.update_target_size
        )

    def select_scale(
        self,
        scale,
    ):
        for index in range(
            self.scale_combo.count()
        ):
            item_scale = self.scale_combo.itemData(
                index
            )

            if isinstance(
                item_scale,
                float,
            ):
                if abs(
                    item_scale
                    - scale
                ) < 0.0001:
                    self.scale_combo.setCurrentIndex(
                        index
                    )
                    return

        self.scale_combo.setCurrentIndex(
            3
        )
        self.custom_scale.setValue(
            scale
        )

    def update_scale_controls(
        self
    ):
        mode = self.scale_combo.currentData()

        self.custom_scale.setEnabled(
            mode == "custom"
        )
        self.actual_distance.setEnabled(
            mode == "distance"
        )
        self.simulated_distance.setEnabled(
            mode == "distance"
        )
        self.calculated_scale_label.setEnabled(
            mode == "distance"
        )

    def get_scale(
        self
    ):
        mode = self.scale_combo.currentData()

        if mode == "custom":
            return self.custom_scale.value()

        if mode == "distance":
            return (
                self.actual_distance.value()
                / self.simulated_distance.value()
            )

        return mode

    def update_target_size(
        self
    ):
        target_type = self.target_type_combo.currentData()
        target_info = TARGET_TYPES.get(
            target_type
        )

        if target_info is None:
            return

        scale = self.get_scale()

        width = (
            target_info["width"]
            * scale
        )
        height = (
            target_info["height"]
            * scale
        )

        self.calculated_scale_label.setText(
            f"{scale * 100:.1f}%"
        )
        self.target_size_label.setText(
            f"{width:.1f} × {height:.1f} mm"
        )

    def get_settings(
        self
    ):
        return {
            "target_type": self.target_type_combo.currentData(),
            "scale": self.get_scale(),
            "thickness": self.thickness.value(),
        }


def show_steel_target_dialog():
    dialog = SteelTargetDialog(
        parent=Gui.getMainWindow(),
    )

    if not dialog.exec():
        return

    settings = dialog.get_settings()

    try:
        create_steel_target(
            target_type=settings[
                "target_type"
            ],
            scale=settings[
                "scale"
            ],
            thickness=settings[
                "thickness"
            ],
        )

    except Exception as error:
        App.Console.PrintError(
            "Steel target error: "
            f"{error}\n"
        )
        raise


class CreateSteelTargetCommand:
    def GetResources(
        self
    ):
        return {
            "MenuText": "Create Steel Target",
            "ToolTip": (
                "Create a scaled steel "
                "dry fire target"
            ),
        }

    def Activated(
        self
    ):
        show_steel_target_dialog()

    def IsActive(
        self
    ):
        return True
