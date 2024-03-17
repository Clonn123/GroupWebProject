import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Content from '../Content/Content';
import axios from 'axios';
import '../Content/Content.css';
import './ContentList.css';

function ContentList({ currentUser }) {
  const [dataList, setDataList] = useState([]);
  const [flexDirection, setFlexDirection] = useState('row');
  const [selectedIcon, setSelectedIcon] = useState('defaultSort');

  const [sort, setSort] = useState('По рейтингу');
  const [sortName, setSortName] = useState('score');
  const { sorttype } = useParams();
  const navigate = useNavigate();

  const [sortBT, setSortBT] = useState('-');
  const [textSort, setTextSort] = useState('По убыванию');
  const [isLoading, setIsLoading] = useState(true);

  const [pageNumber, setPageNumber] = useState(2);
  const [fetch, setFetch] = useState(false);
  const [totalCount, setTotalCount] = useState(2);

  const handleScroll = () => {
    localStorage.setItem('scrollPosition', window.scrollY);
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
      setFetch(true);
    }
  };
  
  useEffect(() => {
    document.addEventListener('scroll', handleScroll);
    return () => {
      document.removeEventListener('scroll', handleScroll);
    };
  }, []);

  useEffect(() => {
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
      window.scrollTo(0, parseInt(scrollPosition));
    }
  }, [dataList]);

  useEffect(() => {
    if (!currentUser || !currentUser.id) {
      return;
    }
    setIsLoading(true);

    setPageNumber(2);
    setTotalCount(2);
    axios
      .get(`http://127.0.0.1:8000/api/data/${sorttype}/?pageNumber=${1}`)
      .then((response) => {
        setDataList(response.data['data']);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Ошибка:', error);
        setIsLoading(false);
      });
  }, [sorttype, currentUser]);

  useEffect(() => {
    if (fetch && pageNumber <= totalCount) {
      axios
        .get(`http://127.0.0.1:8000/api/data/${sorttype}/?pageNumber=${pageNumber}`)
        .then((response) => {
          setDataList((prevDataList) => [...prevDataList, ...response.data['data']]);
          setIsLoading(false);
          setFetch(false);
          setTotalCount(response.data['total_elements']);
          setPageNumber((prevPageNumber) => prevPageNumber + 1);
          // Обновляем позицию прокрутки после загрузки данных
          localStorage.setItem('scrollPosition', window.scrollY);
        })
        .catch((error) => {
          console.error('Ошибка:', error);
          setIsLoading(false);
        });
    }
  }, [fetch, sorttype, currentUser, pageNumber]);

  function toggleFlexDirection() {
    setFlexDirection('column');
    setSelectedIcon('infoSort');
  }

  function defaultFlexDirection() {
    setFlexDirection('row');
    setSelectedIcon('defaultSort');
  }

  function handleSortChange(ru_type, type, BT) {
    setSort(ru_type);
    setSortName(type);
    navigate(`/animes/sort/${BT}${type}`);
  }

  function sortBTChange(type, text, sort) {
    setSortBT(type);
    setTextSort(text);
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
            onClick={defaultFlexDirection}
            width='32'
            height='32'
            src='https://img.icons8.com/fluency-systems-regular/48/grid.png'
            alt='grid'
          />
          <img
            style={{ background: selectedIcon === 'infoSort' ? '#976832' : 'none' }}
            className='infoSort'
            onClick={toggleFlexDirection}
            width='32'
            height='32'
            src='https://img.icons8.com/fluency-systems-regular/48/grid-3.png'
            alt='grid-3'
          />
          <div className='raitingSort' onClick={() => handleSortChange('По рейтингу', 'score', sortBT)}>
            По рейтингу
          </div>
          <div className='dataSort' onClick={() => handleSortChange('По дате', 'descriptionData', sortBT)}>
            По дате
          </div>
          <div className='ABCSort' onClick={() => handleSortChange('По алфавиту', 'title_ru', sortBT)}>
            По алфавиту
          </div>
          <div>|</div>

          <div className='downSort' onClick={() => sortBTChange('-', 'По убыванию', sortName)}>
            По убыванию
          </div>
          <div className='upSort' onClick={() => sortBTChange('', 'По возрастанию', sortName)}>
            По возрастанию
          </div>
        </div>
        <div className='notice2'>
          На данной странице отображены аниме, отсортированные: {sort} и {textSort}
        </div>
        {isLoading && <h2>Loading...</h2>}
      </div>

      <div style={{ flexDirection: flexDirection }} className={`Content-container ${flexDirection}`}>
        {dataList.map((cont, index) => (
          <Content key={index} cont={cont} selectedIcon={selectedIcon} currentUser={currentUser} />
        ))}
      </div>
    </div>
  );
}

export default ContentList;
