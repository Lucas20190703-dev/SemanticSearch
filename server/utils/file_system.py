# server/app/utils/file_system.py

import os
from pathlib import Path
import mimetypes

# Root folder to share
ROOT_DIR = Path("E:/Test/").resolve()

# -----------------------------
# Directory traversal
# -----------------------------
def get_directory_structure(path: Path):
    directories = []
    for entry in sorted(path.iterdir()):
        if entry.is_dir() and not entry.name.startswith('.'):
            directories.append({
                "name": entry.name,
                "path": str(entry.relative_to(ROOT_DIR)).replace("\\", "/"),
                "type": "folder",
                "children": get_directory_structure(entry)
            })
    return directories

# -----------------------------
# List files in a directory
# -----------------------------
def get_files_from_directory(dir_path: str, offset: int = 0, limit: int = 20):
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        return []

    all_files = []
    for f in sorted(path.iterdir()):
        if not f.is_file():
            continue
        mime_type, _ = mimetypes.guess_type(f.name)
        if mime_type and (mime_type.startswith("image") or mime_type.startswith("video")):
            all_files.append((f, mime_type))

    sliced = all_files[offset:offset + limit]

    return [
        {
            "fileName": f.name,
            "filePath": str(f.resolve()).replace("\\", "/"),
            "fileType": mime_type.split("/")[0],  # "image" or "video"
            "fileSize": f.stat().st_size,
            "modified": int(f.stat().st_mtime)
        }
        for f, mime_type in sliced
    ]
