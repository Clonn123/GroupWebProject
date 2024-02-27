import React, { useState } from 'react';
import './Profile.css';
import Avatar from './Avatar';
import Menu from './Menu';
import SettingsPage from './SettingProfile';
import { Link } from 'react-router-dom';
import { ProfileContext } from './context';


function Profile({ currentUser, onLogout }) {
  const [showPersonalInfo, setShowPersonalInfo] = useState(false);

  const [userImage, setUserImage] = useState('');
  const togglePersonalInfo = () => {
    setShowPersonalInfo(!showPersonalInfo);
  };



  return (
    <ProfileContext.Provider value={{ setUserImage, userImage}} >
    <div className='profile'>
      <div className='youself'>
        <div className='chenge_profile'>
          <Avatar />
        </div>
          <h2 className='name'>{currentUser.username}</h2>
          <hr className="separator" />
      <h4 onClick={togglePersonalInfo} style={{ cursor: 'pointer' }}>
        {showPersonalInfo ? 'Личная информация:' : 'Личная информация...'}
      </h4>

      <div className={`info-container ${showPersonalInfo ? 'visible' : ''}`}>
      <div>
          <div>Имя: {currentUser.name}</div>
          <div>Фамилия: {currentUser.surname}</div>
          <div>Пол: {}</div>
          <div>Возраст: {}</div>
        </div>
      </div>
      
      <hr className="separator" />
        <button className='onLogout_but' onClick={onLogout}>
            <Link to="/" className="link">Выйти</Link>
        </button>
      </div>
      <Menu currentUser={currentUser} />
    </div>
    </ProfileContext.Provider>
  );
}

export default Profile;