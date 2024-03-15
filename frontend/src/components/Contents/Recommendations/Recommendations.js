import React, { useEffect, useState } from 'react';
import "./Recommendations.css";
import axios from 'axios';
import ContentRec from '../Content/ContentRec';

function MyRecommendations({ currentUser }) {
  const [dataList, setDataList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!currentUser || !currentUser.id) {
      return; 
    }
    setIsLoading(true);

    axios.get(`http://127.0.0.1:8000/api/rec/anime/?id_user=${currentUser.id}`)
    .then(response => {
      setDataList(response.data);
      setIsLoading(false);
    })
    .catch(error => {
      console.error('Ошибка:', error);
      setIsLoading(false);
    });
  }, [currentUser]);

  return (
    <div className="NN">
      <h2>Персонализированные рекомендации</h2>
      <div>Фильтрация: нет / слабая / средняя / сильная / полная</div>
      <div>
        Чем слабее выбрана фильтрация, тем больше ты получишь результатов, и тем
        неожиданнее они могут оказаться.
      </div>
      <hr className="separator" />
      <div>
        На этой странице для тебя автоматически подбираются рекомендации к
        чтению на основе твоего списка манги. Исходя из поставленных тобой
        оценок, сайт находит других пользователей сайта, имеющих схожие с твоими
        вкусы. На основе списков этих людей составляется каталог того, что,
        возможно, будет тебе интересно.
      </div>
      <hr className="separator" />
      <h2>Не удалось подобрать рекомендации!</h2>
      <div>
        Для успешного подбора рекомендаций необходимо наличие в твоём аниме
        списке 20-30 просмотренных и оценённых произведений.
      </div>

      {isLoading && <h2>Loading...</h2>}
      {!isLoading && dataList && (
      <div className='Rec-container'>
        {dataList.map((cont, index) => (
          <ContentRec key={index} cont={cont} currentUser={currentUser}/>
        ))}
      </div>
      )}
    </div>
  );
}

export default MyRecommendations;

