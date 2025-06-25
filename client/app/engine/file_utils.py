
from pathlib import Path
import mimetypes, os

from PySide6.QtCore import QObject, Slot

def scan_files_recursively(directory, extensions):
    path = Path(directory)
    files = []
    for ext in extensions:
        for img in path.rglob(f'*.{ext}'):
            files.append(img.as_uri())
    
    return files


def scan_media_files_recursively(directory):
    base_path = Path(directory)
    media_files = []

    for file_path in base_path.rglob("*"):
        if file_path.is_file():
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                if mime_type.startswith("image/") or mime_type.startswith("video/"):
                    media_files.append(str(file_path))

    return media_files


def get_file_type(file):
    mime_type, _ = mimetypes.guess_type(file)
    if mime_type:
        if mime_type.startswith("image/"):
            return "image"
        elif mime_type.startswith("video/"):
            return "video"
    return "unknown"

def is_image_video_file(file):
    file_type = get_file_type(file)
    return file_type == "image" or file_type == "video"

def get_keywords_from_path(file, based):
    rel_path = os.path.dirname(os.path.relpath(file, based))
    
    dir_parts = rel_path.split(os.sep)
    
    # Filter out empty parts (e.g. from leading drive letter or root)
    dir_parts = [part for part in dir_parts if part and not part.endswith(":")]
    
    # file name
    file_name_without_ext = os.path.splitext(os.path.basename(file))[0]
    
    dir_parts.append(file_name_without_ext)
    
    return dir_parts
    
def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {units[i]}"


class FileHelper(QObject):
    def __init__(self):
        super().__init__()
    
    @Slot(str)
    def isVideo(self, file):
        return get_file_type(file) == "video"
    
    @Slot(str, result=str)
    def thumbnail(self, video):
        if self.isVideo(video):
            dirname = os.path.dirname(video)
            filename = os.path.basename(video)
            thumb_dir = os.path.join(dirname, filename + "_thumbs")
            return os.path.join(thumb_dir, "scene-001.jpg")
        else:
            return video
    