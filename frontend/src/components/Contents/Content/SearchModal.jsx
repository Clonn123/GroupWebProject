import React from 'react';
import SearchContent from './SearchContent';
import './SearchContent.css';

function SearchResultsDropdown({ results, onItemClick }) {
  return (
    <div className="search-results-dropdown">
      {results.map((cont, index) => (
        <div key={index} onClick={onItemClick}>
          <SearchContent cont={cont} />
        </div>
      ))}
    </div>
  );
}

export default SearchResultsDropdown;
