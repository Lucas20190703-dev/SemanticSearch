import sys
import os
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QSurfaceFormat, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt, QStandardPaths, QCoreApplication
from PySide6.QtQuickControls2 import QQuickStyle

sys.path.append(os.fspath(Path(__file__).parent.parent))

from engine.window_event_filter import WindowEventFilter
from app.engine.manager import EngineManager

from resources import icons # rc file

def main():    
    format = QSurfaceFormat()
    format.setSwapBehavior(QSurfaceFormat.DoubleBuffer) # Double Buffering on
    format.setSwapInterval(0)                            # v-sync off
    QSurfaceFormat.setDefaultFormat(format)
    
    QQuickStyle.setStyle("Basic")
    
    # create event filter for frameless window
    # eventFilter = WindowEventFilter()
    
    
    # create application
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Image Browser")
    app.setOrganizationName("Serhii PySide6 Example")
    app.setOrganizationDomain("org.serhii.pyside.example")
    
    # app.installNativeEventFilter(eventFilter)
    # QCoreApplication.instance().installNativeEventFilter(eventFilter)
    
    app.setWindowIcon(QIcon(":/icons/icon.ico"))
    
    font = app.font()
    font.setPointSize(9)
    app.setFont(font)
    
    # create qml engine
    engine = QQmlApplicationEngine()
    
    engine.addImportPath(str(Path(__file__).resolve().parent / "qml"))
    
    manager = EngineManager(engine)
    
    qml_file = Path(__file__).resolve().parent / "qml/Main.qml"
    
    def on_view_created(url):
        # eventFilter.initWindow(engine)
        manager.initialize()
        
    engine.objectCreated.connect(on_view_created)
    
    engine.load(qml_file.as_uri())
    
    if not engine.rootObjects():

        sys.exit(-1)
    
    
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()