import React, { useState } from 'react';
import './ThemeToggleButton.css'

function ThemeToggleButton({ toggleTheme, isDarkMode }) {

  return (
    <button className='theme-toggle-button' onClick={toggleTheme}>
      {!isDarkMode ? (
        <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/100/sun--v1.png" alt="sun--v1" />
      ) : (
        <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/100/moon-symbol.png" alt="moon-symbol" />
      )}
    </button>
  );
}

export default ThemeToggleButton;

