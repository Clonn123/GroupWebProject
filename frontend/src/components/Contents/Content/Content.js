import React from "react";
import "./Content.css";
import { Link } from "react-router-dom";

function Content({ cont, selectedIcon }) {
  return (
    <div
      className={`${selectedIcon === "infoSort" ? "selected" : "no_selected"}`}
    >
      <div class="hoverable">
        <Link className="Link" to={`/animes/${cont.anime_list_id}`}>
          <div className="item">
            <img src={cont.url_img} alt={cont.title_ru} />
            <div className="smolInfoContainer">
              <h2 className="h2Item">{cont.title_ru}</h2>
              <p className="score">{cont.score}</p>
              <p>{cont.descriptionEpisod}</p>
              <p>{cont.descriptionData}</p>
            </div>
            <div className="allInfoContainer">
              Ну здравствуйте Прекрасные Мадамочки Аж красные Я миллионер Да я
              богат Знакомству с вами Очень рад Она так улыбается и смотрит
              прямо в глаза Да ты мне тоже нравишься я говорю эту фразу У пойдем
              ко мне, эта тусовка уже не по мне Да я весь в огне, "почему бы
              нет" Наталия Я не нормальный шизик Я отнимаю жизни (лалале
              лалалей) Ты так прекрасна Агония В моем подвале трупы Разложены по
              кругу (лалале лалалей) Немного страшно Наталия И ты садишься в
              такси со мной Слушай водитель вези домой Давай побыстрее дави на
              газ Я не хочу сейчас упускать свой шанс Ты так играешь с моей
              рукой Не торопись погоди постой Скоро приедем тут по прямой И мы
              будем вдвоем, и мы будем с тобой Если б ты знала что у меня на уме
              (на уме) Ты б посрывала волосы на голове (у ее) Даже моя бейби не
              знала Как и сейчас Наталия Я не нормальный шизик Я отнимаю жизни
              (лалале лалалей) Ты так прекрасна Агония В моем подвале трупы
              Разложены по кругу (лалале лалалей) Немного страшно Наталия О е
              Почему ты плачешь постоянно? Всё же хорошо смотри: ха ха ха Я не
              наркоман и я не пьяный Просто я чуть-чуть маньяк Прости меня, лети
              душа Прям в небеса, в рай в рай
            </div>
          </div>
        </Link>
        <span class="hover-content">
          Контент, который появится при наведении
        </span>
      </div>
    </div>
  );
}

export default Content;
