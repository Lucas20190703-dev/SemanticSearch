import React from "react";

export default function FileGrid({ files, onSelectFile }) {
  return (
    <div className="grid grid-cols-4 gap-4 p-2">
      {files.map((file) => (
        <div key={file.filePath} className="border rounded p-1 cursor-pointer hover:shadow" onClick={() => onSelectFile(file)}>
          {file.fileType === "image" ? (
            <img src={`http://localhost:3000/api/media/${file.filePath}`} alt={file.fileName} className="h-32 w-full object-cover" />
          ) : (
            <video src={`http://localhost:3000/api/media/${file.filePath}`} className="h-32 w-full object-cover" />
          )}
          <p className="text-sm truncate mt-1">{file.fileName}</p>
        </div>
      ))}
    </div>
  );
}
