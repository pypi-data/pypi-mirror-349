import sys
from PyQt5.QtWidgets import QApplication
from gfESDdataMergeTools.scr.mainwindow import MainWindow

def main():
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("GF.ESDTools.1.0.0")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()