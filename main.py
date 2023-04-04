from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLineEdit, QToolBar, QStatusBar, QLabel, QGridLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox,
    QMessageBox
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")

        file_menu_bar = self.menuBar().addMenu("&File")
        help_menu_bar = self.menuBar().addMenu("&Help")
        edit_menu_bar = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Students", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_bar.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_bar.addAction(about_action)

        search_action = QAction(QIcon("icons/icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_bar.addAction(search_action)

        # create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        # header table
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        # insert table to display main window
        self.setCentralWidget(self.table)

        # create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create status bar and status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit button")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete button")
        delete_button.clicked.connect(self.delete)

        """ find buttons of QPushButton and crab them """
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                # if button (child) have exists in children --> remove them
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_table(self):
        connection = sqlite3.connect("database.db")
        db = connection.execute("SELECT * FROM students")

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(db):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()
    """ user trigger add button --> dialog be displayed to add new student """
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = editDialog()
        dialog.exec()

    def delete(self):
        dialog = deleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add combo box of subjects
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # add mobile number widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Button Submit
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                        (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_windows.load_table()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Windows")
        self.setFixedWidth(300)
        self.setFixedHeight(400)

        layout = QVBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search here")
        layout.addWidget(self.search_box)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_students)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_students(self):
        name = self.search_box.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))
        row = list(result)
        print(row)
        matching_items = main_windows.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in matching_items:
            main_windows.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


class editDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Information Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        index = main_windows.table.currentRow()
        students_name = main_windows.table.item(index, 1).text()

        self.student_index = main_windows.table.item(index, 0).text()
        # add student name widget
        self.student_name = QLineEdit(students_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add combo box of subjects
        course_name = main_windows.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # add mobile number widget
        mobile = main_windows.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Button Submit
        submit_button = QPushButton("Confirm")
        submit_button.clicked.connect(self.update_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_index))
        connection.commit()
        cursor.close()
        connection.close()
        main_windows.load_table()


class deleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete students data")
        grid = QGridLayout()
        label_delete = QLabel("Are you sure want to delete")
        button_yes = QPushButton("Yes")
        button_yes.clicked.connect(self.yes_action)
        button_no = QPushButton("No")
        button_yes.clicked.connect(self.no_action)

        grid.addWidget(label_delete, 0, 0, 1, 2)
        grid.addWidget(button_yes, 1, 0)
        grid.addWidget(button_no, 1, 1)

        self.setLayout(grid)

    def yes_action(self):
        index = main_windows.table.currentRow()
        student_id = main_windows.table.item(index, 0).text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_windows.load_table()

        self.close()

        confirm = QMessageBox()
        confirm.setWindowTitle("Success")
        confirm.setText("Delete Successfully")
        confirm.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app is created by NGO MANH CUONG, finished at 4/4/2023.
        Fell free to modify and reuse this app.
        --------------Thank you---------------
        """
        self.setText(content)


app = QApplication(sys.argv)
main_windows = MainWindow()
main_windows.show()
main_windows.load_table()
sys.exit(app.exec())