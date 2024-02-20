import React, { useState } from 'react';
import './Profile.css';
import Avatar from './Avatar';
import { Link } from 'react-router-dom';



function Profile({ currentUser, onLogout }) {
  const [showPersonalInfo, setShowPersonalInfo] = useState(false);

  const togglePersonalInfo = () => {
    setShowPersonalInfo(!showPersonalInfo);
  };

  return (
    <div className='profile'>
      <div className='youself'>
        <div className='chenge_profile'>
          <Avatar />
          <Link to="/setting"><button className='setting'>Настройки</button></Link>
          
        </div>
          <h2 className='name'>{currentUser.username}</h2>
          <hr className="separator" />
      <h4 onClick={togglePersonalInfo} style={{ cursor: 'pointer' }}>
        {showPersonalInfo ? 'Личная информация:' : 'Личная информация...'}
      </h4>
      {showPersonalInfo && (
        <div>
          <div>Имя: {currentUser.name}</div>
          <div>Фамилия: {currentUser.surname}</div>
          <div>Пол: {}</div>
          <div>Возраст: {}</div>
        </div>
      )}
      <hr className="separator" />
          <button className='onLogout_but' onClick={onLogout}>Выйти</button>
      </div>
  
      <div className='menu'>
        <h3>Меню</h3>
        <hr className="separator" />
        <ln>
          <div>Главная</div>
          <div>Список Аниме</div>
          <div>Друзья</div>
        </ln>
        
        <hr className="separator" />



      </div>


    </div>
    
    
  );
}

export default Profile;