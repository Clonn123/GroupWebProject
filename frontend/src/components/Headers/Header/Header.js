import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header({ currentUser }) {
  return (
    <div className="header-container">
        <div className="header">
        <h1><Link to="/" className="header-link" >Стартовая страница</Link></h1> {/* Обертываем надпись в Link и устанавливаем to="/" для перехода на стартовую страницу */}
          <div className="categories">
            <div><Link to="/animes"  className="category">Аниме</Link></div>
            <div><Link to="/book" className="category">Книги</Link></div>
          </div>
          <div className="search-bar">
            <input type="text" placeholder="🔍 Поиск..." />
          </div>
          <div className="registration-link">
          {currentUser ? (
              <Link to="/profile">{currentUser.username}</Link>//имя пользователя сюда и его аву
            ) : (
              <>
                <Link to="/registration">Регистрация</Link>
                <Link to="/login">Вход</Link>
              </>
            )}
          </div>
        </div>
    </div>
  );
}

export default Header;