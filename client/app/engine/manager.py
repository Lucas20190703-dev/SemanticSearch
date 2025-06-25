
from PySide6.QtCore import *
from app.engine.search_engine import SearchEngine
from app.engine.image_caption import ImageCaptioning
from app.engine.expansionnetv2_module import init_expansionnetv2_model
from app.engine.worker import Worker
from app.engine.scene_dectector import SceneDetector
from app.engine.file_utils import FileHelper
from app.engine.directorymodel import DirectoryModel

from app.engine.api import *

class EngineManager(QObject):
    initializingStarted = Signal()
    modelLoaded = Signal()
    
    def __init__(self, qmlEngine):
        super().__init__()
        
        self._searchEngine = SearchEngine()
        self._captionEngine = ImageCaptioning()
        self._sceneDetector = SceneDetector()
        self._fileHelper = FileHelper()
        
        self._directoryModel = DirectoryModel(API_FETCH_DIRECTORY)
        
        qmlEngine.rootContext().setContextProperty("engineManager", self)
        qmlEngine.rootContext().setContextProperty("singleCaptioning", self._captionEngine)
        qmlEngine.rootContext().setContextProperty("searchEngine", self._searchEngine)
        qmlEngine.rootContext().setContextProperty("sceneDetector", self._sceneDetector)
        qmlEngine.rootContext().setContextProperty("fileHelper", self._fileHelper)
        qmlEngine.rootContext().setContextProperty("directoryModel", self._directoryModel)
        
        # above Qt 6.0, use StandardPaths of QML
        pictureLocation = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0]
        qmlEngine.rootContext().setContextProperty("pictureLocation", pictureLocation)
        
        
    @Slot()
    def initialize(self):
        self.initializingStarted.emit()
        worker = Worker(init_expansionnetv2_model)
        worker.signals.finished.connect(self.on_model_loaded)
        QThreadPool.globalInstance().start(worker)        
    
    @Slot()
    def close(self):
        self._searchEngine.close()
        self._sceneDetector.clean()
        
    @Slot()
    def on_model_loaded(self):
        print("Model initialized.")
        self.modelLoaded.emit()
        self._searchEngine.start()