import React, { useState } from "react";
import axios from "axios";
import "./RS.css";
import StatusComponent from './StatusComponent.js'

const RatingComponent = () => {
  const [rating, setRating] = useState(1);
  const [status, setStatus] = useState('');

  const handleRatingChange = (e) => {
    const newRating = parseInt(e.target.value, 10);
    setRating(newRating);
    
    console.log('Установлена оценка:', newRating);
  };

  return (
    <div>
      <div className="rating-component">
      <StatusComponent setStatus={setStatus} />
      {status === 'просмотренно' && (
        <>
        <h4>Установить оценку:</h4>
        <input className="slider"
          type="range"
          min="1"
          max="10"
          value={rating}
          onChange={handleRatingChange}
        />
        <p>Ваша оценка: {rating}</p>
        </>
      )}
    </div>

    </div>
    
  );
};
export default RatingComponent;
