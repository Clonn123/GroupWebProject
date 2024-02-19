import React, { useState } from 'react';

function ThemeToggleButton({ toggleTheme, isDarkMode }) {

  return (
    <button onClick={toggleTheme}>
      {!isDarkMode ? (
        <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/sun--v1.png" alt="sun--v1" />
      ) : (
        <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/moon-symbol.png" alt="moon-symbol" />
      )}
    </button>
  );
}

export default ThemeToggleButton;

