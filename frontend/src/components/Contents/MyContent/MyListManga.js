import React, { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import Content from '../Content/ContentManga.js';
import Nav from '../Navigations/Nav.js';
import axios from 'axios';
import '../ContentList/ContentList.css';

function MyListManga( {currentUser} ) {
  const [dataList, setDataList] = useState([]);
  const [flexDirection, setFlexDirection] = useState('column');
  const [selectedIcon, setSelectedIcon] = useState('infoSort');

  const [sort, setSort] = useState('По рейтингу');
  const [sortName, setSortNAme] = useState('score');
  const { sorttype } = useParams();
  const { id } = useParams();
  const navigate = useNavigate()

  const [sortBT, setSortBT] = useState('-');
  const [textSort, settextSort] = useState('По убыванию');
  const [isLoading, setIsLoading] = useState(true);
  


  useEffect(() => {
    if (!currentUser || !currentUser.id) {
      return; 
    }
    setIsLoading(true);

    axios.get(`http://127.0.0.1:8000/api/data/mylist-manga/${id}/${sorttype}`)
      .then(response => {
        setDataList(response.data);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Ошибка:', error);
        setIsLoading(false);
      });
  }, [sorttype, currentUser]);

  

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
    navigate(`/myListManga/${id}/${BT}${type}`);
  }
  function sortBTChange(type, text, sort){
    setSortBT(type)
    settextSort(text)
    navigate(`/myListManga/${id}/${type}${sort}`);
  }


  return (
    <div className='head'>
      <div className='notice'>
        <h1 className='title'>Мой список манги</h1>
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
            alt="grid"
          />
          <div className='raitingSort' onClick={() => handleSortChange('По рейтингу', 'score', sortBT)}>По рейтингу</div>
          <div className='dataSort' onClick={() => handleSortChange('По дате', 'descriptionData', sortBT)}>По дате</div>
          <div className='ABCSort' onClick={() => handleSortChange('По алфавиту', 'title_ru', sortBT)}>По алфавиту</div>
          <div>|</div>

          <div className='downSort' onClick={() => sortBTChange('-', 'По убыванию', sortName)}>По убыванию</div>
          <div className='upSort' onClick={() => sortBTChange('', 'По возростанию', sortName)}>По возростанию</div>
        </div>
        <div className='notice2' >Мой список, отсортированный: {sort} и {textSort}</div>
        {isLoading && <h2>Loading...</h2>}
      </div>

      <div style={{ flexDirection: flexDirection }} className={`Content-container ${flexDirection}`}>
        {dataList.map((cont, index) => (
          <Content key={index} cont={cont} selectedIcon={selectedIcon} currentUser={currentUser}/>
        ))}
      </div>
      
    </div>
  );
}

export default MyListManga;