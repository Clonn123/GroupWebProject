import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async (query) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/search?query=${query}`);
      setSearchResults(response.data);
    } catch (error) {
      console.error('Ошибка при выполнении запроса:', error);
    }
  };

  const handleChange = (event) => {
    setSearchQuery(event.target.value);
    handleSearch(event.target.value);
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Поиск..."
        value={searchQuery}
        onChange={handleChange}
      />
      {searchQuery && (
        <div className="search-results">
        {searchResults.map((result) => (
          <div key={result.anime_list_id}>
            <p>{result.title_ru}</p>
            {/* Другие свойства результата поиска */}
          </div>
        ))}
      </div>
      )}
      
    </div>
  );
};

export default SearchBar;
