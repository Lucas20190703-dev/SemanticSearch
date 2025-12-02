import React, { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if(query.trim()) onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="flex mb-4">
      <input
        type="text"
        placeholder="Search captions..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-grow border rounded-l px-2 py-1"
      />
      <button type="submit" className="bg-blue-500 text-white px-4 rounded-r">Search</button>
    </form>
  );
}
