import React, { useEffect, useState } from "react";
import { fetchDirectories } from "../api/server";

export default function Sidebar({ onSelectDir }) {
  const [dirs, setDirs] = useState([]);

  useEffect(() => {
    fetchDirectories().then(setDirs);
  }, []);

  const renderDir = (dir) => (
    <li key={dir.path} className="pl-2 cursor-pointer hover:bg-gray-200 rounded" onClick={() => onSelectDir(dir.path)}>
      {dir.name}
      {dir.children.length > 0 && (
        <ul className="pl-4">{dir.children.map(renderDir)}</ul>
      )}
    </li>
  );

  return (
    <aside className="w-64 bg-gray-100 p-2 overflow-auto h-screen">
      <h2 className="text-lg font-bold mb-2">Folders</h2>
      <ul>{dirs.map(renderDir)}</ul>
    </aside>
  );
}
