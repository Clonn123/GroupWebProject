import React, { useState, useEffect } from 'react';
import './Profile.css';
import Avatar from './Avatar';
import Menu from './Menu';
import SettingsPage from './SettingProfile';
import { Link } from 'react-router-dom';
import { ProfileContext } from './context';
import ShikimoriButton from './ShikimoriButton'; // Импортируем компонент OAuthButton
import axios from 'axios';


function Profile({ currentUser, onLogout }) {
  const [showPersonalInfo, setShowPersonalInfo] = useState(false);
  const [codeInUrl, setCodeInUrl] = useState('');
  const [animeList, setAnimeList] = useState([]);

  const [userImage, setUserImage] = useState('');
  const togglePersonalInfo = () => {
    setShowPersonalInfo(!showPersonalInfo);
  };

  useEffect(() => {
    // Проверяем, есть ли параметр code в URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('code')) {
      setCodeInUrl(urlParams.get('code'));
    }
  }, []);

  const handleClick = async () => {
    // console.info("Code: "+codeInUrl)
    if (codeInUrl != '') {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/anime-list/', { codeInUrl });
        console.info(response);
        setAnimeList(response.data.anime_titles);
      } catch (error) {
        console.error('Ошибка при обработке запроса:', error);
      }
    } else {
      console.error('Ошибка: параметр "code" отсутствует в URL');
    }
  };

  return (
    <ProfileContext.Provider value={{ setUserImage, userImage, animeList }} >
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
          <div>Пол: {currentUser.gender}</div>
          <div>Возраст: {currentUser.age}</div>
        </div>
      </div>
      
      <hr className="separator" />
        <ShikimoriButton />

        <button className='onLogout_but' onClick={onLogout}>
            <Link to="/" className="link">Выйти</Link>
        </button>

        <button className='fetch_anime_button' onClick={handleClick}>
            Получить список аниме
        </button>

        {animeList.length > 0 && (
            <div>
              <h3>Список аниме:</h3>
              <ul>
                {animeList.map((anime, index) => (
                  <li key={index}>{anime.title}</li>
                ))}
              </ul>
            </div>
          )}
      </div>
      <Menu currentUser={currentUser} />
    </div>
    </ProfileContext.Provider>
  );
}

export default Profile;