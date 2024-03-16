import React from 'react';
import SearchContent from '../../Contents/Content/SearchContent';
import "./SearchContent.css";

const SearchResultsDropdown = ({ results, onItemClick }) => {
  return (
    <div className="search-results-dropdown">
      {results.map((cont, index) => (
        <div key={index} onClick={onItemClick}>
          <SearchContent cont={cont} />
        </div>
      ))}
    </div>
  );
};

export default SearchResultsDropdown;

