import { useState } from "react";
import SearchBar from "../components/SearchBar";
import { semanticSearch } from "../api/server";
import FileGrid from "../components/FileGrid";

export default function Search() {
  const [results, setResults] = useState([]);

  const doSearch = async (q) => {
    const r = await semanticSearch(q);
    setResults(r.results);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Semantic Search</h1>

      <div className="mt-4">
        <SearchBar onSearch={doSearch} />
      </div>

      {results.length > 0 && (
        <FileGrid files={results} onOpen={() => {}} />
      )}
    </div>
  );
}
