from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QPushButton,
    QComboBox
)
import sys


class Distance(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        label_distance = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        label_time = QLabel("Time (Hour):")
        self.time_line_edit = QLineEdit()

        self.box = QComboBox()
        self.box.addItem("Metric (km)")
        self.box.addItem("Imperial (miles)")

        button_calculate = QPushButton("Calculate")
        button_calculate.clicked.connect(self.calculate_speed)
        self.output_label = QLabel("")

        grid.addWidget(label_distance, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.box, 0, 2, )
        grid.addWidget(label_time, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(button_calculate, 3, 1)
        grid.addWidget(self.output_label, 4, 0)

        self.setLayout(grid)

    def calculate_speed(self):
        distance = float(self.distance_line_edit.text())
        time = float(self.time_line_edit.text())
        speed = distance / time
        if self.box.currentText() == "Metric (km)":
            speed = round(speed, 2)
            self.output_label.setText(f"Average Speed: {speed} Km/h")
        elif self.box.currentText() == "Imperial (miles)":
            speed = round(speed * 0.621371, 2)
            self.output_label.setText(f"Average Speed: {speed} mph")
        else:
            self.output_label.setText("Value invalid")


app = QApplication(sys.argv)
distance_cal = Distance()
distance_cal.show()
sys.exit(app.exec())