import React from 'react';
import Content from './content';
import '../css/content.css';

function ContentList({ dataList }) {
    return (
        <div className='head'>
            <div className='notice'>
                <h1 className='title'>Название страницы</h1>
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