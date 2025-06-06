import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory, QSystemSemaphore, Qt
from ui.main_window import MainWindow
from core.ffmpeg_checker import check_ffmpeg

def main():
    shared_mem = QSharedMemory("YoutubeGO4.4")
    
    if not shared_mem.create(1):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        for widget in app.topLevelWidgets():
            if isinstance(widget, MainWindow):
                if widget.isMinimized():
                    widget.showNormal()
                widget.setWindowState(widget.windowState() & ~Qt.WindowMinimized)
                widget.activateWindow()
                widget.raise_()
                widget.show()
                return
        return
    
    app = QApplication(sys.argv)
    
    ffmpeg_found, ffmpeg_path = check_ffmpeg()
    if not ffmpeg_found:
        print("FFmpeg not found. Please ensure it is installed and in PATH.")
    else:
        print(f"FFmpeg found at: {ffmpeg_path}")
    
    win = MainWindow(ffmpeg_found=ffmpeg_found, ffmpeg_path=ffmpeg_path)
    win.show()
    
    app.aboutToQuit.connect(lambda: shared_mem.detach())
    sys.exit(app.exec())

if __name__ == "__main__":
    main()