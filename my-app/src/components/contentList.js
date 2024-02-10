import React from 'react';
import Content from './content';
import '../css/content.css';

function ContentList({ dataList }) {
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