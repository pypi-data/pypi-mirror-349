import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QButtonGroup, QTextEdit, QMessageBox,
                             QFileDialog, QComboBox)
from PyQt5.QtGui import QIcon

# 修改导入路径为绝对路径
from gfESDdataMergeTools.scr.tlpdatamerge import TLPDataMerge
from gfESDdataMergeTools.scr.hbmdatamerge import HBMDataMerge
import pkg_resources


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window icon
        self.setWindowIcon(self._get_taskbar_icon())

        self.setWindowTitle("Singapore ESD lab Merge Test Data Tools")
        # Set fixed window size (width 600, height 400)
        self.setFixedSize(600, 400) 

        # Creating a Menu Bar
        menubar = self.menuBar()

        # Adding the File Menu
        file_menu = menubar.addMenu('&File')
        open_folder_action = file_menu.addAction('Open Folder')
        open_folder_action.triggered.connect(self.open_folder_dialog)

        help_menu = menubar.addMenu('&Help')
        # Adding an About Action
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about_dialog)

        # Creating the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Radio Button
        self.tlp_radio = QRadioButton("TLP data merge")
        self.hbm_radio = QRadioButton("HBM data merge")
        self.tlp_radio.setChecked(True)  # TLP is selected by default
        
        radio_group = QButtonGroup()
        radio_group.addButton(self.tlp_radio)
        radio_group.addButton(self.hbm_radio)

        # Listen for radio button click events
        # radio_group.buttonClicked.connect(self._update_tester_by_radio)
        self.tlp_radio.toggled.connect(self._update_tester_by_radio)
        self.hbm_radio.toggled.connect(self._update_tester_by_radio)

        radio_layout = QHBoxLayout()
        radio_label = QLabel("Merge Option: ")
        radio_layout.addWidget(radio_label)
        radio_layout.addWidget(self.tlp_radio)
        radio_layout.addWidget(self.hbm_radio)
        main_layout.addLayout(radio_layout)

        # Data path input
        path_layout = QHBoxLayout()
        path_label = QLabel("Data Path:")
        self.path_edit = QLineEdit()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit)
        main_layout.addLayout(path_layout)

        # Output file name
        output_layout = QHBoxLayout()
        output_label = QLabel("Output File Name:")
        self.output_edit = QLineEdit()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_edit)
        main_layout.addLayout(output_layout)

        # Tester drop-down list
        tester_layout = QHBoxLayout()
        tester_label = QLabel("Tester:")
        self.tester_combo = QComboBox()
        self.tester_combo.addItems(["TLP01", "TLP02", "TLP03", "vf-TLP", "Hanwa_HBM"])
        tester_layout.addWidget(tester_label)
        tester_layout.addWidget(self.tester_combo)
        tester_layout.addStretch(1)  # Compress drop-down box width
        tester_layout.setSpacing(10)  # Adjust the spacing between labels and drop-down boxes
        main_layout.addLayout(tester_layout)

        # Set the initial value of Tester according to the default selected radio button
        self._update_tester_by_radio()

        # Execute button
        self.execute_btn = QPushButton("Execute Data Merge")
        self.execute_btn.clicked.connect(self.execute_merge)

        # Creating a Button Container Layout
        button_container = QHBoxLayout()
        button_container.addStretch(1)  # Adding left flex space
        button_container.addWidget(self.execute_btn)
        
        # Setting the button style
        self.execute_btn.setFixedWidth(150)  # Fixed Width
        self.execute_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-weight: bold;
                min-width: 80px;
            }
        """)
        
        main_layout.addLayout(button_container)

        # Add a QTextEdit component in the GUI to display the processing log
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        main_layout.addWidget(self.log_view)

    def _update_tester_by_radio(self, _=None):
        """Update the default value of the Tester drop-down list based on the selected radio button"""

        if self.tlp_radio.isChecked():
            self.tester_combo.setCurrentText("TLP01")
        else:
            self.tester_combo.setCurrentText("Hanwa_HBM")
        
    def _get_taskbar_icon(self):
        """Get the taskbar icon (.ico format is preferred)"""
        icon_paths = [
            r"app_logo/GFS.ico",  # Windows Recommended
            r"app_logo/GFS.png",  # Linux/macOS alternative
            r"app_logo/GF_logo.ico",     # Compatible with old paths
            r"app_logo/GlobalFoundries_logo.png"
        ]
        
        for path in icon_paths:
            try:
                full_path = pkg_resources.resource_filename("gfESDdataMergeTools", path)
                #full_path = os.path.join(os.path.dirname(__file__), path)
                if os.path.exists(full_path):
                    return QIcon(full_path)
            except Exception as e:
                print(f"Error loading icon {path}: {str(e)}")
        
        # Return to default icon when file not found
        print("Warning: Taskbar icon file not found")
        return QIcon()

    def show_about_dialog(self):
        """Show About dialog box"""

        text_to_user = (
            "Note to user: This software, utilized by the Singapore ESD/Latchup Lab,\n"
            "merges test data from the Celestron-I TLP system and the Hanwa HBM system.\n"
            "The merged data can then be uploaded to the Jasper Web Application.\n"
            "\nFirst Create Date: 29 April 2025\n"
            "Software owner: Yang Ting\n"
            "Software version: v1.1\n"
            "\nUpdate Date: 30 April 2025\n"
            "Bug fix: \n1. Added functionality to detect duplicate device names.\n"
            "2. Ability to detect if a file ends without a newline character (\\n)."
        )
        
        bug_fix_log = (
            "Software version: v1.0\n"
            "Tools first delivery.\n"
            "\nSoftware version: v1.1\n"
            "\nUpdate Date: 30 April 2025\n"
            "Bug fix: \n1. Added functionality to detect duplicate device names.\n"
            "2. Ability to detect if a file ends without a newline character (\\n)."
        )

        about_box = QMessageBox()
        about_box.setWindowTitle("About")
        about_box.setIcon(QMessageBox.Information)
        about_box.setText(text_to_user)

        about_box.setDetailedText(bug_fix_log)

        about_box.addButton(QMessageBox.Ok)
        about_box.exec_()

    def open_folder_dialog(self):
        """Open the folder selection dialog"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Data Folder",
            r"D:/YangTing/Download",  # By default, it starts from the esd_lu directory.
            QFileDialog.ShowDirsOnly
        )
        
        if folder_path:  # Update only if the user actually selects a folder
            self.path_edit.setText(folder_path)
            self.output_edit.setText(f"{os.path.basename(folder_path)}")

    def log_message(self, message):
        """Add log information to the log window"""
        self.log_view.append(message)
        QApplication.processEvents()  # Force refresh UI

    def execute_merge(self):
        """Slot function that performs the merge operation"""
        data_path = self.path_edit.text()
        output_base = self.output_edit.text()
        tester = self.tester_combo.currentText()  # Get the currently selected Tester value
        print("Main window: ", tester)

        # Create output directory path
        output_dir = os.path.join(os.getcwd(), "Output")
        output_file = os.path.join(output_dir, output_base)

        # Clear old logs
        self.log_view.clear()

        if self.tlp_radio.isChecked():
            # Here the TLP merge class is called
            print(f"Perform TLP data merge\nPath: {data_path}\nOutput File: {output_file}")
            self.log_message("=== Start TLP data processing ===")
            self.tlp_merge = TLPDataMerge(
                data_path, 
                output_file,
                tester,
                log_callback=self.log_message  # Add logging callback
            )
            self.tlp_merge.process()
        else:
            # Here we call the HBM merge class
            print(f"Perform HBM data merge\nPath: {data_path}\nOutput File: {output_file}")
            self.log_message("=== Start HBM data processing ===")
            self.hbm_merge = HBMDataMerge(
                data_path, 
                output_file,
                tester,
                log_callback=self.log_message  # Add logging callback
            )
            self.hbm_merge.process()