import React, { useState } from 'react';
import axios from 'axios';
import './RS.css'

const StatusComponent = ({ animeId }) => {
    const [status, setStatus] = useState('');
  
    const handleStatusChange = async () => {
      try {
        await axios.post(`http://localhost:8000/api/anime/${animeId}/status`, { status });
        alert('Статус успешно установлен!');
      } catch (error) {
        console.error('Ошибка:', error);
      }
    };
  
    return (
        <div className="status-component">
        <h3>Установить статус:</h3>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">Выберите статус</option>
          <option value="просмотренно">Просмотренно</option>
          <option value="запланированно">Запланированно</option>
          <option value="брошенно">Брошенно</option>
        </select>
        <button onClick={handleStatusChange}>Установить</button>
      </div>
    );
  };
export default StatusComponent;