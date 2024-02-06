import React from 'react';
import './css/header.css';

function Header() {
  return (
    <div className="header-container">
        <div className="header">
        <h1>Название сайта</h1>

        <div className="categories">
        <   div><a href="animes" className="category">Аниме</a></div>
            <div><a href="book" className="category">Книги</a></div>
        </div>

        <div className="search-bar">
            <input type="text" placeholder="🔍 Поиск..." />
        </div>

        <div className="registration-link">
            <a href="/registration" className="reg">Регистрация</a>
            <a href="/login" className="reg" >Вход</a>
        </div>
        </div>
    </div>
    
  );
}

export default Header;
