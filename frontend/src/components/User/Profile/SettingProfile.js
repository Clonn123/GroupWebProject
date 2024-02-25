import React, { useState } from 'react';
import './SettingProfile.css';
import SaveButton from './Save';
import Avatar from './Avatar';


function SettingsPage( {currentUser} ) {
  const [photo, setPhoto] = useState('');
  const [nickname, setNickname] = useState(currentUser.username);
  const [firstName, setFirstName] = useState(currentUser.name);
  const [lastName, setLastName] = useState(currentUser.surname);
  const [gender, setGender] = useState('');
  const [birthdate, setBirthdate] = useState('');
  const [previewPhoto, setPreviewPhoto] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Здесь вы можете добавить код для отправки данных формы на сервер или их обработки
    console.log('Form submitted:', { photo, nickname, firstName, lastName, gender, setBirthdate });
  };

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPhoto(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewPhoto(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className='settint-container'>
      <Avatar photoUrl={previewPhoto} />
      <form className='formsetting' onSubmit={handleSubmit}>
      <h2>Настройки</h2>
        <div>
          <label htmlFor="photo">Фото:</label>
          <input type="file" id="photo" onChange={handlePhotoChange} />
        </div>
        <div>
          <label htmlFor="nickname">Никнейм:</label>
          <input type="text" id="nickname" value={nickname} onChange={(e) => setNickname(e.target.value)} />
        </div>
        <div>
          <label htmlFor="firstName">Имя:</label>
          <input type="text" id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        </div>
        <div>
          <label htmlFor="lastName">Фамилия:</label>
          <input type="text" id="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} />
        </div>
        <div>
          <label htmlFor="gender">Пол:</label>
          <select id="gender" value={gender} onChange={(e) => setGender(e.target.value)}>
            <option value="male">Мужской</option>
            <option value="female">Женский</option>
            <option value="pupu">Другое</option>
          </select>
        </div>
        <div>
          <label htmlFor="age">Возраст:</label>
          <input type="date" id="birthdate" value={birthdate} onChange={(e) => setBirthdate(e.target.value)} />
        </div>
        <SaveButton />
      </form>
    </div>
  );
}

export default SettingsPage;
