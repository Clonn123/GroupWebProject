import React, { useState } from 'react';
import axios from 'axios';
import './RS.css'

const RatingComponent = ({ animeId }) => {
  const [rating, setRating] = useState(0);

  const handleRatingChange = async () => {
    try {
      await axios.post(`http://localhost:8000/api/anime/${animeId}/rating`, { rating });
      alert('Оценка успешно установлена!');
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  return (
    <div className="rating-component">
      <h3>Установить оценку:</h3>
      <input type="number" min="1" max="10" value={rating} onChange={(e) => setRating(e.target.value)} />
      <button onClick={handleRatingChange}>Установить</button>
    </div>
  );
};
export default RatingComponent