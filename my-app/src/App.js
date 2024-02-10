import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'; // Используем Routes вместо Switch
import Header from './components/header.js';
import './css/App.css';
import RegistrationForm from './components/RegistrationForm.js';
import ContentList from './components/contentList.js';
import UserList from './components/UserList.js';
import BotHeader from './components/botheader.js';
import LoginForm from './components/LoginForm.js';
import Profile from './components/Profile.js';

function App() {
  const [users, setUsers] = useState([
    { id: 1, name: 'Артем', surname: 'Полозников', username: 'Clonn123', password: 'Clonn123', email: 'art-clon@mail.ru' },
    { id: 2, name: 'Андрей', surname: 'Смирнов', username: 'Gifon', password: 'Gifon', email: 'gifon@mail.ru' },
  ]);

  const [currentUser, setCurrentUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));

  const dataList = [
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название1',
      description: 'Описание1',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
  ];

  useEffect(() => {
    // Проверяем наличие токена в localStorage при загрузке компонента
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      // Вызываем функцию для автоматического входа пользователя
      autoLogin(accessToken);
    }
  }, []);

  const handleAddUser = (newUser) => {
    setUsers([...users, newUser]); // Добавляем нового пользователя в список
  };
  
  const handleLogin = (user, rememberMe) => {
    setCurrentUser(user);
    if (rememberMe) {    
        // Сохранение токена доступа в локальном хранилище
        localStorage.setItem('accessToken', generateToken(user.id));
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    // Удаляем токен из localStorage при выходе пользователя
    localStorage.removeItem('accessToken');
  };

  const autoLogin = () => {
    const accessToken = localStorage.getItem('accessToken');
  
    if (accessToken) {
      // Находим пользователя по токену
      const user = users.find(u => generateToken(u.id) === accessToken);
  
      if (user) {
        setCurrentUser(user);
      }
    }
  };

  const generateToken = (userId) => {
    return `token_${userId}`;
  };  
  
  return (
    <Router>
      <div>
        <Header currentUser={currentUser} onLogout={handleLogout} />
        <Routes>
          <Route path="/registration" element={<RegistrationForm onUserAdd={handleAddUser} />} />
          <Route path="/login" element={<LoginForm users={users} onLogin={handleLogin} />} />
          <Route path="/" element={<UserList users={users} />} />
          <Route path="/animes" element={<ContentList dataList={dataList}  />} />
          {currentUser && <Route path="/profile" element={<Profile currentUser={currentUser} onLogout={handleLogout} />} />}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
