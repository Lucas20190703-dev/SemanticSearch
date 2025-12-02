import axios from "axios";

const API_BASE = "http://localhost:3000/api";

export const fetchDirectories = async () => {
  const res = await axios.get(`${API_BASE}/directories`);
  return res.data;
};

export const fetchFiles = async (dirPath, offset = 0, limit = 20) => {
  const res = await axios.get(`${API_BASE}/files/${dirPath}?offset=${offset}&limit=${limit}`);
  return res.data;
};

export const searchCaptions = async (query, top_k = 5, format="json") => {
  const res = await axios.post(`${API_BASE}/search`, {
    content: query,
    top_k,
    format
  });
  return res.data;
};
