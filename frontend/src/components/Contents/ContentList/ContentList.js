import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Content from '../Content/Content';
import axios from 'axios';
import '../Content/Content.css';
import './ContentList.css';

function ContentList() {
  const [dataList, setDataList] = useState([]);
  const [flexDirection, setFlexDirection] = useState('row');
  const [selectedIcon, setSelectedIcon] = useState('defaultSort');

  const [sort, setSort] = useState('По рейтингу');
  const [sortName, setSortNAme] = useState('score');
  const { sorttype } = useParams();
  const navigate = useNavigate()

  const [sortBT, setSortBT] = useState('-');
  const [textSort, settextSort] = useState('По убыванию');
  


  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/api/data/${sorttype}`)
      .then(response => {
        setDataList(response.data);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }, [sorttype]);

  function toggleFlexDirection() {
    setFlexDirection('column');
    setSelectedIcon('infoSort'); 
  }

  function defoultFlexDirection() {
    setFlexDirection('row');
    setSelectedIcon('defaultSort');
  }

  function handleSortChange(ru_type, type, BT){
    setSort(ru_type);
    setSortNAme(type)
    navigate(`/animes/sort/${BT}${type}`);
  }
  function sortBTChange(type, text, sort){
    setSortBT(type)
    settextSort(text)
    navigate(`/animes/sort/${type}${sort}`);
  }

  return (
    <div className='head'>
      <div className='notice'>
        <h1 className='title'>Аниме</h1>
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
          <div className='raitingSort' onClick={() => handleSortChange('По рейтингу', 'score', sortBT)}>По рейтингу</div>
          <div className='dataSort' onClick={() => handleSortChange('По дате', 'descriptionData', sortBT)}>По дате</div>
          <div className='ABCSort' onClick={() => handleSortChange('По алфавиту', 'title_ru', sortBT)}>По алфавиту</div>
          <div>|</div>

          <div className='downSort' onClick={() => sortBTChange('-', 'По убыванию', sortName)}>По убыванию</div>
          <div className='upSort' onClick={() => sortBTChange('', 'По возростанию', sortName)}>По возростанию</div>


        </div>
        <div className='notice2' >На данной странице отображены аниме, отсортированные: {sort} и {textSort}</div>
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
