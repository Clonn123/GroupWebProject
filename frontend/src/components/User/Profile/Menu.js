import React, { useState } from 'react';
import './Menu.css';
import SettingsPage from './SettingProfile';

function Menu({currentUser}) {
  const [showSettint, setSettting] = useState(false);

  const togglesSettting = () => {
    setSettting(!showSettint);
  };
  
    return (
      <>
      <div className={`settings-container ${showSettint ? 'visible' : ''}`}>
        <SettingsPage currentUser={currentUser}/>
      </div>
        <div className='menu'>
        <h3>Меню</h3>
        <hr className="separator" />
        <ln>
          <div>Главная</div>
          <div>Список Аниме</div>
          <div>Рекомендации</div>
          <div>Друзья</div>
        </ln>
        
        <hr className="separator" />
        <div onClick={togglesSettting}>
          {showSettint ? 'Скрыть настройки' : 'Настройки'}
        </div>
      </div>
      
      </>
        
      
      
    );
  }
  
  export default Menu;