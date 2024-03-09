import React, { useState } from 'react';

const StatusComponent = ({ setStatus }) => {
  const [status, setStatusState] = useState('');

  const handleStatusChange = (newStatus) => {
    setStatusState(newStatus);
    setStatus(newStatus);
  };

  return (
    <div className="status-component">
      <h4>Установить статус:</h4>
      <div className="card-container">
        <div className={`card ${status === 'просмотренно' ? 'selected green' : ''}`} onClick={() => handleStatusChange('просмотренно')}>
          Просмотренно
        </div>
        <div className={`card ${status === 'запланированно' ? 'selected blue' : ''}`} onClick={() => handleStatusChange('запланированно')}>
          Запланированно
        </div>
        <div className={`card ${status === 'брошенно' ? 'selected red' : ''}`} onClick={() => handleStatusChange('брошенно')}>
          Брошенно
        </div>
      </div>
    </div>
  );
};

export default StatusComponent;

