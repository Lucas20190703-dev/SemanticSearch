import os
from pathlib import Path
import mimetypes
from urllib.parse import unquote
import datetime

# Set this to the folder you want to share
ROOT_DIR = Path("E:/Test/").resolve()

def get_directory_structure(path: Path):
    directories = []
    for entry in sorted(path.iterdir()):
        if entry.is_dir() and not entry.name.startswith('.'):  # Exclude hidden folders
            directories.append({
                "name": entry.name,
                "path": str(entry.relative_to(ROOT_DIR)),
                "type": "folder",
                "children": get_directory_structure(entry)
            })
    return directories


def get_files_from_directory( dir_path: str, offset: int = 0, limit: int = 20):
    if not dir_path.exists() or not dir_path.is_dir():
        return None

    directory = Path(dir_path)

    if not directory.is_dir():
        return []

    all_files = []
    for f in sorted(directory.iterdir()):
        if not f.is_file():
            continue
        mime_type, _ = mimetypes.guess_type(f.name)
        if mime_type and (mime_type.startswith("image") or mime_type.startswith("video")):
            all_files.append((f, mime_type))

    sliced = all_files[offset:offset + limit]

    return [
        {
            "fileName": f.name,
            "filePath": str(f).replace("\\", "/"),
            "fileType": mime_type.split("/")[0],  # e.g., "image" or "video"
            "fileSize": os.path.getsize(f),
            "modified": int(os.path.getctime(f))
        }
        for f, mime_type in sliced
    ]
    