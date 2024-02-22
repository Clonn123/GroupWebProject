import React, { useState, useEffect } from 'react';
import Content from '../Content/Content';
import axios from 'axios';
import '../Content/Content.css';

function ContentList() {
    // грузим с бека данные
  const [dataList, setDataList] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/data/')
      .then(response => {
        setDataList(response.data);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }, []);

    
    return (
        <div className='head'>
            <div className='notice'>
                <h1 className='title'>Название страницы</h1>
                <div className='navigation'>
                <img width="32" height="32" src="https://img.icons8.com/fluency-systems-regular/48/grid.png" alt="grid"/>
                <img width="32" height="32" src="https://img.icons8.com/fluency-systems-regular/48/grid-2.png" alt="grid-2"/>
                <img width="32" height="32" src="https://img.icons8.com/fluency-systems-regular/48/grid-3.png" alt="grid-3"/>
                </div>
                <notice>Описание страницы</notice>
            </div>
            <div className='Content-container'>
            {dataList.map((cont, index) => (
            <Content key={index} cont={cont} />
            ))}
            </div>
        </div>
    );
  }

export default ContentList;