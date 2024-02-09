import React from 'react';
import '../css/content.css';

function Content({ user }) {
  return (
    <div className="Content-container">
        <div className="item">
        <img src="https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg" alt="Описание изображения" />
        <h2>Название</h2>
        <p>Дополнительная информация</p>
        {/* Дополнительные поля с информацией */}       
        </div>
    </div>
  );
}

export default Content;