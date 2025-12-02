import { getStreamUrl } from "../api/server";

export default function VideoPlayer({ file }) {
  return (
    <video
      className="w-full max-h-[80vh]"
      controls
      src={getStreamUrl(file.path)}
    />
  );
}
