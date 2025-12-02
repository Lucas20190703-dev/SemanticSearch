import React from "react";

export default function CaptionModal({ file, caption, onClose }) {
  if (!file) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-4 rounded w-96">
        <h3 className="font-bold mb-2">{file.fileName}</h3>
        {file.fileType === "image" ? (
          <img src={`http://localhost:3000/api/media/${file.filePath}`} className="w-full mb-2" />
        ) : (
          <video src={`http://localhost:3000/api/media/${file.filePath}`} controls className="w-full mb-2" />
        )}
        <p className="mb-2">{caption}</p>
        <button onClick={onClose} className="bg-red-500 text-white px-3 py-1 rounded">Close</button>
      </div>
    </div>
  );
}
