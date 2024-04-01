import React, { useEffect, useState } from "react";
import "./Recommendations.css";
import axios from "axios";
import ContentRec from "../Content/ContentRecManga";

function MyRecommendationsManga({ currentUser }) {
  const [dataList, setDataList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRec, setIsRec] = useState(false);

  const [pageNumber, SetpageNumber] = useState(2);
  const [fetch, SetFetch] = useState(false);

  const [CBFMethod, SetCBFMethod] = useState(true);
  const [SVDMethod, SetSVDMethod] = useState(false);

  const [method, SetMethod] = useState('CBF');

  const Scrole = (e) => {
    if (
      e.target.documentElement.scrollHeight -
        (e.target.documentElement.scrollTop + window.innerHeight) <
      100
    ) {
      localStorage.setItem(
        "scrollPosition",
        e.target.documentElement.scrollTop
      );
      SetFetch(true);
    }
  };

  useEffect(() => {
    document.addEventListener("scroll", Scrole);
    return function () {
      document.removeEventListener("scroll", Scrole);
    };
  }, []);

  useEffect(() => {
    if (!currentUser || !currentUser.id) {
      return;
    }
    setIsLoading(true);
    SetpageNumber(2);

    axios
      .get(
        `http://127.0.0.1:8000/api/rec/manga/?id_user=${
          currentUser.id
        }&pageNumber=${1}&method=${method}`
      )
      .then((response) => {
        setDataList(response.data);
        setIsLoading(false);

        if (response.data == false) {
          setIsRec(false);
        } else {
          setIsRec(true);
        }
      })
      .catch((error) => {
        console.error("Ошибка:", error);
        setIsLoading(false);
      });
  }, [currentUser, method]);

  useEffect(() => {
    if (fetch) {
      axios
        .get(
          `http://127.0.0.1:8000/api/rec/manga/?id_user=${currentUser.id}&pageNumber=${pageNumber}&method=${method}`
        )
        .then((response) => {
          setDataList([...dataList, ...response.data]);
          setIsLoading(false);
          SetFetch(false);
          SetpageNumber((prevState) => prevState + 1);
        })
        .catch((error) => {
          console.error("Ошибка:", error);
          setIsLoading(false);
        });
    }
  }, [fetch, currentUser, method]);

  function FunCBFMethod(type) {
    if (type == "CBF") {
      SetCBFMethod(true);
      SetMethod('CBF')
      SetSVDMethod(false);
    } else {
      SetCBFMethod(false);
      SetMethod('SVD')
      SetSVDMethod(true);
    }
  }

  return (
    <div className="NN">
      <h2>Персонализированные рекомендации</h2>
      <div className="Method">
        {" "}
        <strong>Метод:</strong>
        <div className="CBF" onClick={() => FunCBFMethod("CBF")}>
          CBF
        </div>
        <div> / </div>
        <div className="SVD" onClick={() => FunCBFMethod("SVD")}>
          SVD
        </div>
      </div>
      <div className="infoMetod">
        {CBFMethod && (
          <div>
            Content-Based Filtering, CBF - это метод рекомендательных систем, который основан на анализе
            содержания элементов и предпочтений пользователя. Основная идея
            заключается в том, чтобы рекомендовать элементы, которые похожи на
            те, которые пользователь уже оценил положительно.
          </div>
        )}
        {SVDMethod && <div>Singular Value Decomposition, SVD - это метод рекомендательных систем, который использует матричное разложение 
          для анализа взаимосвязей между пользователями и элементами. Он помогает предсказывать, какие элементы могут понравиться пользователю, 
          основываясь на его предыдущих оценках и на общих паттернах взаимодействия пользователей с элементами.
          </div>}
      </div>
      <hr className="separator" />
      <div>
        На данной странице были сформированы рекомендации на основе ваших интересов.
      </div>
      <hr className="separator" />
      {isRec == false && (
        <>
          <h2>Не удалось подобрать рекомендации!</h2>
          <div>
            Для успешного подбора рекомендаций необходимо наличие в твоём аниме
            списке не менее 20 просмотренных и оценённых произведений.
          </div>
        </>
      )}

      {isLoading && <h2>Loading...</h2>}
      {!isLoading && dataList && (
        <div className="Rec-container">
          {dataList.map((cont, index) => (
            <ContentRec key={index} cont={cont} currentUser={currentUser} />
          ))}
        </div>
      )}
    </div>
  );
}

export default MyRecommendationsManga;
