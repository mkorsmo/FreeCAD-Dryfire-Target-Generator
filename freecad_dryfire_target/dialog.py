from PySide import QtWidgets


class TargetSettingsDialog(QtWidgets.QDialog):
    def __init__(
        self,
        title,
        target_width,
        target_height,
        default_scale,
        default_thickness,
        default_groove_width,
        default_groove_depth,
        parent=None,
    ):
        super().__init__(parent)

        self.target_width = target_width
        self.target_height = target_height

        self.setWindowTitle(title)
        self.setMinimumWidth(340)

        self.build_ui(
            default_scale,
            default_thickness,
            default_groove_width,
            default_groove_depth,
        )

        self.update_scale_controls()
        self.update_target_size()
        self.update_groove_depth_limit()

    def build_ui(
        self,
        default_scale,
        default_thickness,
        default_groove_width,
        default_groove_depth,
    ):
        layout = QtWidgets.QVBoxLayout(self)

        scale_group = QtWidgets.QGroupBox("Scale")
        scale_layout = QtWidgets.QFormLayout(scale_group)

        self.scale_combo = QtWidgets.QComboBox()
        self.scale_combo.addItem("1/2 scale", 1 / 2)
        self.scale_combo.addItem("1/3 scale", 1 / 3)
        self.scale_combo.addItem("1/4 scale", 1 / 4)
        self.scale_combo.addItem("Custom", None)

        self.custom_scale = QtWidgets.QDoubleSpinBox()
        self.custom_scale.setDecimals(4)
        self.custom_scale.setRange(0.01, 1.0)
        self.custom_scale.setSingleStep(0.01)
        self.custom_scale.setValue(default_scale)

        scale_layout.addRow("Scale:", self.scale_combo)
        scale_layout.addRow("Custom:", self.custom_scale)

        self.target_size_label = QtWidgets.QLabel()
        scale_layout.addRow("Target size:", self.target_size_label)

        layout.addWidget(scale_group)

        print_group = QtWidgets.QGroupBox("Print Geometry")
        print_layout = QtWidgets.QFormLayout(print_group)

        self.thickness = QtWidgets.QDoubleSpinBox()
        self.thickness.setDecimals(2)
        self.thickness.setRange(0.2, 10.0)
        self.thickness.setSingleStep(0.1)
        self.thickness.setSuffix(" mm")
        self.thickness.setValue(default_thickness)

        self.groove_width = QtWidgets.QDoubleSpinBox()
        self.groove_width.setDecimals(2)
        self.groove_width.setRange(0.1, 5.0)
        self.groove_width.setSingleStep(0.1)
        self.groove_width.setSuffix(" mm")
        self.groove_width.setValue(default_groove_width)

        self.groove_depth = QtWidgets.QDoubleSpinBox()
        self.groove_depth.setDecimals(2)
        self.groove_depth.setRange(0.05, default_thickness)
        self.groove_depth.setSingleStep(0.05)
        self.groove_depth.setSuffix(" mm")
        self.groove_depth.setValue(default_groove_depth)

        print_layout.addRow("Thickness:", self.thickness)
        print_layout.addRow("Groove width:", self.groove_width)
        print_layout.addRow("Groove depth:", self.groove_depth)

        layout.addWidget(print_group)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.select_scale(default_scale)

        self.scale_combo.currentIndexChanged.connect(
            self.update_scale_controls
        )
        self.scale_combo.currentIndexChanged.connect(
            self.update_target_size
        )
        self.custom_scale.valueChanged.connect(
            self.update_target_size
        )
        self.thickness.valueChanged.connect(
            self.update_groove_depth_limit
        )

    def select_scale(self, scale):
        for index in range(self.scale_combo.count()):
            item_scale = self.scale_combo.itemData(index)

            if item_scale is not None and abs(item_scale - scale) < 0.0001:
                self.scale_combo.setCurrentIndex(index)
                return

        self.scale_combo.setCurrentIndex(
            self.scale_combo.count() - 1
        )
        self.custom_scale.setValue(scale)

    def update_scale_controls(self):
        custom = self.scale_combo.currentData() is None
        self.custom_scale.setEnabled(custom)

    def update_target_size(self):
        scale = self.get_scale()

        width = self.target_width * scale
        height = self.target_height * scale

        self.target_size_label.setText(
            f"{width:.1f} × {height:.1f} mm"
        )

    def update_groove_depth_limit(self):
        maximum_depth = max(
            0.05,
            self.thickness.value() - 0.05,
        )

        self.groove_depth.setMaximum(maximum_depth)

    def get_scale(self):
        scale = self.scale_combo.currentData()

        if scale is None:
            return self.custom_scale.value()

        return scale

    def get_settings(self):
        return {
            "scale": self.get_scale(),
            "thickness": self.thickness.value(),
            "groove_width": self.groove_width.value(),
            "groove_depth": self.groove_depth.value(),
        }