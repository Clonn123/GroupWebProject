import React, { useState } from 'react';
import "./RS.css";

const ReviewComponent = ({ onSubmit }) => {
  const [reviewText, setReviewText] = useState('');

  const handleInputChange = (e) => {
    setReviewText(e.target.value);
  };

  const handleSubmit = () => {
    onSubmit(reviewText);
    // Сбросить текстовое поле после отправки отзыва
    setReviewText('');
  };

  return (
    <>
    <div className="review-component">
      <h4 className="review-title">Написать отзыв:</h4>
      <textarea
        className="review-textarea"
        value={reviewText}
        onChange={handleInputChange}
        placeholder="Введите ваш отзыв"
        rows={4}
      />
      <button className="submit-button" onClick={handleSubmit}>Отправить</button>
    </div>
    </>
    
  );
};

export default ReviewComponent;
