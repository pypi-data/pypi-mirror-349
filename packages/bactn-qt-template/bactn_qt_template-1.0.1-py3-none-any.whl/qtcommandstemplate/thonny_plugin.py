from thonny import get_workbench
from tkinter import messagebox

def insert_bac_tn_pyqt_template():
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if editor:
        template = """from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic

# Your logic goes here:

def on_button_click():
    QMessageBox.information(None, "Hello", "Button Clicked!")

# Qt Config:
app = QApplication([])
u = uic.loadUi("hamming.ui")
u.show()

# Connect buttons here:
u.pushButton.clicked.connect(on_button_click)

# Start event loop:
app.exec_()
"""
        editor.get_text_widget().insert("insert", template)
        messagebox.showinfo(
            "Template Inserted",
            "✅ PyQt5 template successfully inserted into the editor!\nGood luck coding :3"
        )
def load_plugin():
    get_workbench().add_command(
        command_id="insert_bac_tn_pyqt_template",
        menu_name="tools",
        handler=insert_bac_tn_pyqt_template,
        command_label="Insérer modèle PyQt5 - BacTN"
    )