export default function ImageViewer({ file }) {
  const url = "http://localhost:8000/file?path=" + encodeURIComponent(file.path);

  return (
    <div className="p-4">
      <img src={url} className="max-w-full max-h-[80vh] mx-auto" />
    </div>
  );
}
