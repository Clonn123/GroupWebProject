import React, { useState } from 'react';
import './Save.css'; // Подключаем файл стилей

const SaveButton = () => {
  const [isSaved, setIsSaved] = useState(false);

  const handleClick = () => {
    setIsSaved(!isSaved); // Переключаем состояние кнопки при клике
  };

  return (
    <button type="submit" className={`savebut ${isSaved ? 'saved' : ''}`} onClick={handleClick}>
      {isSaved ? 'Сохранено!' : 'Сохранить'}
    </button>
  );
};

export default SaveButton;