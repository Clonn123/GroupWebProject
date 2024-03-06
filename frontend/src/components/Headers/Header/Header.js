import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import ThemeToggleButton from './ThemeToggleButton.js'
import SearchBar from './SearchBar.js'

function Header({ currentUser, toggleTheme, isDarkMode }) {
  return (
    <div className="header-container">
        <div className="header">
        <h1><Link to="/" className="header-link" >Стартовая страница</Link></h1> {/* Обертываем надпись в Link и устанавливаем to="/" для перехода на стартовую страницу */}
          <div className="categories">
            <div><Link to="/animes"  className="category">Аниме</Link></div>
            <div><Link to="/book" className="category">Книги</Link></div>
            <div><Link to="/recommendations" className="category">Рекомендации</Link></div>
          </div>
          <SearchBar />
          <div className="registration-link">
          {currentUser ? (
              <Link to="/profile">{currentUser.username}</Link>//имя пользователя сюда и его аву
            ) : (
              <>
                <Link to="/registration">Регистрация</Link>
                <Link to="/login">Вход</Link>
              </>
            )}
            <ThemeToggleButton toggleTheme={toggleTheme} isDarkMode={isDarkMode} />
          </div>
          
        </div>
    </div>
  );
}

export default Header;