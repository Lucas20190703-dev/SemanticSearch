import os, json
from pathlib import Path
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images

from PySide6.QtCore import QObject, Signal, Slot, QThreadPool
from app.engine.worker import Worker

def extract_scene_keyframes(video_path, output_dir, threshold=30.0, check_cancelled=None):
    """
    Detects scene changes and saves middle-frame keyframes to output_dir.
        1. Keyframe images (middle frame of each scene)
        2. Scene metadata (timecodes + image paths) to scenes.json
    Args:
        video_path (str): Path to the video file.
        output_dir (str): Directory where images will be saved.
        threshold (float): Scene detection sensitivity (lower = more scenes).
    """
    output_dir = Path(output_dir)
    scenes_json_path = output_dir / "scenes.json"

    # 🔁 If already processed, return existing scene info
    if scenes_json_path.exists():
        with open(scenes_json_path, "r", encoding="utf-8") as f:
            print("Using cached scene info:", scenes_json_path)
            return json.load(f)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Start scene detection
    video_manager = VideoManager([str(video_path)])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    base_timecode = video_manager.get_base_timecode()
    video_manager.set_downscale_factor(2)
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    print(f"Detected {len(scene_list)} scenes.")

    # Cancel check before doing heavy saving
    if check_cancelled and check_cancelled():
        print("Cancelled before saving images.")
        video_manager.release()
        return None

    # Save keyframes
    
    save_images(
        video= video_manager,
        scene_list=scene_list,
        output_dir=str(output_dir),
        image_name_template="scene-$SCENE_NUMBER",
        num_images=1,
        width = 480
    )

    # Build and save JSON
    scene_info = []
    for i, (start, end) in enumerate(scene_list):
        if check_cancelled and check_cancelled():
            print("Cancelled during scene info generation.")
            video_manager.release()
            return None

        image_name = f"scene-{i+1:03d}.jpg"
        image_path = output_dir / image_name
        scene_info.append({
            "scene_number": i + 1,
            "start_time": str(start),
            "end_time": str(end),
            "duration": round(end.get_seconds() - start.get_seconds(), 3),
            "thumbnail": image_path.resolve().as_uri()
        })

    with open(scenes_json_path, "w", encoding="utf-8") as f:
        json.dump(scene_info, f, indent=2)

    video_manager.release()
    print(f"Scene info saved to: {scenes_json_path}")
    
    return scene_info
    
    
class SceneDetector(QObject):
    
    finished = Signal(str)
    error = Signal(str)
    canceled = Signal()

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self._current_worker = None

    @Slot(str)
    def generateKeyframes(self, file: str):
        
        print("Generating scenes from", file)
        
        thumb_dir = self.getThumbnailFolder(file)

        def task(check_cancelled):
            scenes = extract_scene_keyframes(file, thumb_dir, check_cancelled=check_cancelled)
            return { "file": file, "scenes": scenes }

        # Prevent duplicates
        if self._current_worker:
            self._current_worker.cancel()

        worker = Worker(task)
        self._current_worker = worker

        worker.signals.result.connect(self.onFinished)
        worker.signals.error.connect(self.error.emit)
        worker.signals.canceled.connect(self.canceled.emit)
        worker.signals.finished.connect(lambda: setattr(self, "_current_worker", None))

        self.threadpool.start(worker)


    @Slot()
    def cancel(self):
        if self._current_worker:
            self._current_worker.cancel()
            
    @Slot()
    def clean(self):
        self.threadpool.clear()
        self.threadpool.waitForDone()

    def getThumbnailFolder(self, file: str):
        dirname = os.path.dirname(file)
        filename = os.path.basename(file)
        thumb_dir = os.path.join(dirname, filename + "_thumbs")
        os.makedirs(thumb_dir, exist_ok=True)
        return thumb_dir

    @Slot(object)
    def onFinished(self, result):
        jsonstr = json.dumps(result)
        print (type(jsonstr))
        self.finished.emit(jsonstr)