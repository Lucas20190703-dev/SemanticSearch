import { getThumbnailUrl } from "../api/server";

export default function FileCard({ file, onClick }) {
  return (
    <div
      className="border rounded-lg overflow-hidden cursor-pointer hover:shadow"
      onClick={() => onClick(file)}
    >
      <img
        className="w-full h-40 object-cover"
        src={getThumbnailUrl(file.path)}
      />
      <div className="p-2 text-sm text-gray-700">{file.name}</div>
    </div>
  );
}
