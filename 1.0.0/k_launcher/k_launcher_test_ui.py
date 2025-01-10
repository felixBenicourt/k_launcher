import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QTabWidget, QTextEdit, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt

class KLauncherUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("K_Launcher")
        self.setGeometry(100, 100, 900, 600)
        
        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Header
        self.init_header(layout)

        # Tabs
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        self.init_environment_tab()
        self.init_dcc_launcher_tab()
        self.init_git_management_tab()

        # Console
        self.init_console(layout)

        # Footer
        self.init_footer(layout)

    def init_header(self, parent_layout):
        header = QHBoxLayout()

        logo_label = QLabel("<b>K_Launcher</b>")
        logo_label.setStyleSheet("font-size: 24px;")

        current_config_label = QLabel("<i>Current Config: None</i>")
        current_config_label.setAlignment(Qt.AlignRight)

        header.addWidget(logo_label)
        header.addWidget(current_config_label)
        parent_layout.addLayout(header)

    def init_environment_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        config_group = QGroupBox("Configuration Management")
        config_layout = QFormLayout()
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        self.config_dropdown = QComboBox()
        self.config_dropdown.addItems(["dev", "prod", "test"])
        config_layout.addRow("Select Config:", self.config_dropdown)

        self.load_config_btn = QPushButton("Load Config")
        self.save_config_btn = QPushButton("Save Config")
        config_layout.addRow(self.load_config_btn, self.save_config_btn)

        env_table = QTableWidget(5, 2)
        env_table.setHorizontalHeaderLabels(["Variable", "Value"])
        env_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(env_table)

        self.tab_widget.addTab(tab, "Environment")

    def init_dcc_launcher_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        dcc_group = QGroupBox("DCC Tool Launcher")
        dcc_layout = QFormLayout()
        dcc_group.setLayout(dcc_layout)
        layout.addWidget(dcc_group)

        self.dcc_dropdown = QComboBox()
        self.dcc_dropdown.addItems(["Maya", "Houdini", "Nuke"])
        dcc_layout.addRow("Select DCC:", self.dcc_dropdown)

        self.package_input = QLineEdit()
        dcc_layout.addRow("Packages:", self.package_input)

        self.launch_btn = QPushButton("Launch")
        dcc_layout.addWidget(self.launch_btn)

        self.tab_widget.addTab(tab, "DCC Launcher")

    def init_git_management_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        repo_group = QGroupBox("Git Repository Management")
        repo_layout = QFormLayout()
        repo_group.setLayout(repo_layout)
        layout.addWidget(repo_group)

        self.repo_path_input = QLineEdit()
        repo_layout.addRow("Repo Path:", self.repo_path_input)

        self.branch_dropdown = QComboBox()
        self.branch_dropdown.addItems(["main", "dev", "feature"])
        repo_layout.addRow("Branch:", self.branch_dropdown)

        git_btn_layout = QHBoxLayout()
        self.pull_btn = QPushButton("Pull")
        self.commit_btn = QPushButton("Commit")
        self.tag_btn = QPushButton("Tag")
        git_btn_layout.addWidget(self.pull_btn)
        git_btn_layout.addWidget(self.commit_btn)
        git_btn_layout.addWidget(self.tag_btn)
        layout.addLayout(git_btn_layout)

        self.tab_widget.addTab(tab, "Git Management")

    def init_console(self, parent_layout):
        console_label = QLabel("Console:")
        parent_layout.addWidget(console_label)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        parent_layout.addWidget(self.console)

    def init_footer(self, parent_layout):
        footer = QLabel("<i>Status: Ready</i>")
        footer.setAlignment(Qt.AlignRight)
        parent_layout.addWidget(footer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KLauncherUI()
    window.show()
    sys.exit(app.exec_())
