import React, { useState, useEffect } from 'react';
import Content from '../Content/Content';
import axios from 'axios';
import '../Content/Content.css';
import './ContentList.css';

function ContentList() {
  const [dataList, setDataList] = useState([]);
  const [flexDirection, setFlexDirection] = useState('row');
  const [selectedIcon, setSelectedIcon] = useState('defaultSort');


  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/data/')
      .then(response => {
        setDataList(response.data);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }, []);

  function toggleFlexDirection() {
    setFlexDirection('column');
    setSelectedIcon('infoSort'); 
  }

  function defoultFlexDirection() {
    setFlexDirection('row');
    setSelectedIcon('defaultSort');
  }

  return (
    <div className='head'>
      <div className='notice'>
        <h1 className='title'>Название страницы</h1>
        <div className='navigation'>
          <img
            style={{ background: selectedIcon === 'defaultSort' ? '#976832' : 'none' }}
            className='defaultSort'
            onClick={defoultFlexDirection}
            width="32"
            height="32"
            src="https://img.icons8.com/fluency-systems-regular/48/grid.png"
            alt="grid"
          />
          <img
            style={{ background: selectedIcon === 'infoSort' ? '#976832' : 'none' }}
            className='infoSort'
            onClick={toggleFlexDirection}
            width="32"
            height="32"
            src="https://img.icons8.com/fluency-systems-regular/48/grid-3.png"
            alt="grid-3"
          />
        </div>
        <notice>Описание страницы</notice>
      </div>
      <div style={{ flexDirection: flexDirection }} className={`Content-container ${flexDirection}`}>
        {dataList.map((cont, index) => (
          <Content key={index} cont={cont} selectedIcon={selectedIcon} />
        ))}
      </div>
    </div>
  );
}

export default ContentList;
