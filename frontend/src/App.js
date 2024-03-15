import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'; 
import Header from './components/Headers/Header/Header.js';
import './css/App.css';
import './css/LightTheme.css'; 
import './css/DarkTheme.css';
import ThemeToggleButton from './components/Headers/Header/ThemeToggleButton.js' 
import RegistrationForm from './components/Authorization/RegistrationForm/RegistrationForm.js';
import ContentList from './components/Contents/ContentList/ContentList.js';
import PageContent from './components/Contents/PageContent/PageContent.js';
import UserList from './components/User/UserList/UserList.js';
import MyList from './components/Contents/MyContent/MeList.js';
import Recommendations from './components/Contents/Recommendations/Recommendations.js';
import BotHeader from './components/Headers/BotHeader/BotHeader.js';
import LoginForm from './components/Authorization/LoginForm/LoginForm.js';
import Profile from './components/User/Profile/Profile.js';
import axios from 'axios';

function App() {

  const [users, setUsers] = useState([
    { id: 1, name: 'Артем', surname: 'Полозников', username: 'Clonn123', password: 'Clonn123', email: 'art-clon@mail.ru', gender: "Мужчина", age: "21" },
    { id: 2, name: 'Андрей', surname: 'Смирнов', username: 'Gifon', password: 'Gifon', email: 'gifon@mail.ru', gender: "Мужчина", age: "21"  }, 
  ]);

  const [currentUser, setCurrentUser] = useState();
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));

  

  useEffect(() => {
    // Проверяем наличие токена в localStorage при загрузке компонента
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      // Вызываем функцию для автоматического входа пользователя
      autoLogin(accessToken);
    }
  }, [currentUser]);
  
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
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  useEffect(() => {
    const root = document.documentElement;

    if (isDarkMode) {
      root.style.setProperty('--background-image', 'linear-gradient(135deg, #96816e, #96816E, #987F69)');
    } else {
      root.style.setProperty('--background-color', '#98C1D9');
    }
  }, [isDarkMode]);  
  
  return (
      <Router>
      <div className={`app-container ${isDarkMode ? 'dark-theme' : 'light-theme'}`}>
        <Header currentUser={currentUser} toggleTheme={toggleTheme} isDarkMode={isDarkMode} onLogout={handleLogout} />
        <div className='all_buddy'>
        <Routes>
          <Route path="/registration" element={<RegistrationForm />} />
          <Route path="/login" element={<LoginForm users={users} onLogin={handleLogin} />} />
          <Route path="/" element={<UserList users={users} />} />
          <Route path="/anime/recommendations" element={<Recommendations currentUser={currentUser} />} />
          <Route path="/myList/:id/:sorttype" element={<MyList currentUser={currentUser} />} />
          <Route path="/animes/sort/:sorttype" element={<ContentList currentUser={currentUser}/>} />
          <Route path="/animes/:id" element={<PageContent currentUser={currentUser}/>} />
          {currentUser && <Route path="/profile" element={<Profile currentUser={currentUser} onLogout={handleLogout} />} />}
        </Routes>
        </div>   
      </div>
    </Router>
  );
}

export default App;
