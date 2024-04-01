import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchResultsDropdown from '../../Contents/Content/SearchModal';


const SearchBar = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleDocumentClick = (event) => {
    const searchBar = document.querySelector('.search-bar');
    if (searchBar && !searchBar.contains(event.target)) {
      // Если клик был выполнен вне компонента поиска, очистите строку поиска
      setSearchQuery('');
    }
  };
  useEffect(() => {
    document.addEventListener('click', handleDocumentClick);
    return () => {
      document.removeEventListener('click', handleDocumentClick);
    };
  }, []);

  const handleSearch = async (query) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/search-manga?query=${query}`);
      setSearchResults(response.data);
    } catch (error) {
      console.error('Ошибка при выполнении запроса:', error);
    }
  };

  const handleChange = (event) => {
    setSearchQuery(event.target.value);
    handleSearch(event.target.value);
  };
  const handleItemClick = () => {
    setSearchQuery(''); 
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
        <SearchResultsDropdown results={searchResults} onItemClick={handleItemClick} />
      )}
      
    </div>
  );
};

export default SearchBar;
