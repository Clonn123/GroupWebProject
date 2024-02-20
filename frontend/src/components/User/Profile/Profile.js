import React from 'react';
import './Profile.css';
import Avatar from './Avatar'; 

function Profile({ currentUser, onLogout }) {
  return (
    <div className='profile'>
      <div className='youself'>
        <div className='chenge_profile'>
          <Avatar />
          <button className='setting'>Настройки</button>
        </div>
          <h2 className='name'>{currentUser.username}</h2>
          <hr className="separator" />
          <h4>Личная информация:</h4>
          <ln>
          <div>Имя: {currentUser.name}</div>
          <div>Фамилия: {currentUser.surname}</div>
          <div>Пол: {}</div>
          <div>Возраст: {}</div>
        </ln>
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