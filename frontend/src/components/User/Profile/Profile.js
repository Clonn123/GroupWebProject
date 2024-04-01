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
  const [mangaList, setMangaList] = useState([]);

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
        const response = await axios.post('http://127.0.0.1:8000/api/anime-list/', {
        codeInUrl: codeInUrl,
        userId: currentUser.id
        });
        console.info(response);
        setAnimeList(response.data.anime_titles);
        setMangaList(response.data.manga_titles);
      } catch (error) {
        console.error('Ошибка при обработке запроса:', error);
      }
    } else {
      console.error('Ошибка: параметр "code" отсутствует в URL');
    }
  };

  return (
    <ProfileContext.Provider value={{ setUserImage, userImage, animeList, mangaList }} >
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
        <button className='onLogout_but' onClick={onLogout}>
            <Link to="/" className="link">Выйти</Link>
        </button>
      
      <div>      
        <ShikimoriButton />
        <button className='fetch_anime_button' onClick={handleClick}>
            Синхронизировать
        </button>

        {/* {animeList.length > 0 && (
            <div>
              <h3>Список аниме:</h3>
              <ul>
                {animeList.map((anime, index) => (
                  <li key={index}>{["Название: " + anime.title + " ID: " + anime.title_id + " Статус: " + anime.status + " Оценка: " + anime.score]}</li>
                ))}
              </ul>
            </div>
          )} */}
          {mangaList.length > 0 && (
            <div>
              <h3>Ваш список манги загружен с Шикимори!</h3>
              {/* <h3>Список манги:</h3> */}
              {/* <ul>
                {mangaList.map((manga, index) => (
                  <li key={index}>{["Название: " + manga.title + " ID: " + manga.title_id + " Статус: " + manga.status + " Оценка: " + manga.score]}</li>
                ))}
              </ul> */}
            </div>
          )}
      </div>
      {/* <style>
        {`
          html {
            height: 100%;
            margin: 0 auto;
            font-family: 'Montserrat', sans-serif;
          }
        `}
      </style> */}

      </div>
      <Menu currentUser={currentUser} />
    </div>
    </ProfileContext.Provider>
  );
}

export default Profile;