import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import FileGrid from "../components/FileGrid";
import CaptionModal from "../components/CaptionModal";
import SearchBar from "../components/SearchBar";
import { fetchFiles, searchCaptions } from "../api/server";

export default function Home() {
  const [currentDir, setCurrentDir] = useState("");
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [caption, setCaption] = useState("");

  useEffect(() => {
    if (currentDir) {
      fetchFiles(currentDir).then(setFiles);
    }
  }, [currentDir]);

  const handleSearch = async (query) => {
    const results = await searchCaptions(query, 10);
    // results from backend: [{name, path, caption, ...}]
    setFiles(results.map(r => ({
      fileName: r.name,
      filePath: r.path,
      fileType: r.path.endsWith(".mp4") ? "video" : "image"
    })));
  };

  const handleSelectFile = (file) => {
    setSelectedFile(file);
    // fetch caption if needed
    const f = files.find(f => f.filePath === file.filePath);
    setCaption(f.caption || "No caption available");
  };

  return (
    <div className="flex h-screen">
      <Sidebar onSelectDir={setCurrentDir} />
      <main className="flex-1 p-4 overflow-auto">
        <SearchBar onSearch={handleSearch} />
        <FileGrid files={files} onSelectFile={handleSelectFile} />
      </main>
      <CaptionModal file={selectedFile} caption={caption} onClose={() => setSelectedFile(null)} />
    </div>
  );
}
