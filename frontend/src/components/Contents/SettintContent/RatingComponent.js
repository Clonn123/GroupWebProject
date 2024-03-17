import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "./RS.css";
import StatusComponent from "./StatusComponent.js";

const RatingComponent = ({ currentUser, info }) => {
  const { id } = useParams();
  const [rating, setRating] = useState(info.score);
  const [status, setStatus] = useState(info.status);
  const [isDel, setIsDel] = useState(info);

  const [Status, setStatusState] = useState(info.status);

  const [id_user, setId_user] = useState(currentUser.id);
  const [id_anime, setId_anime] = useState(id);

  const handleSubmit = async (newRating) => {
    try {
      axios
        .put("http://127.0.0.1:8000/api/score/", {
          anime_id: id_anime,
          user_id: id_user,
          score: newRating,
        })
        .then((response) => {})
        .catch((error) => {});
    } catch (error) {}
  };

  const handleRatingChange = (e) => {
    const newRating = parseInt(e.target.value, 10);
    setRating(newRating);
    handleSubmit(newRating);

    console.log("Установлена оценка:", newRating);
  };

  const delObject = async () =>{
    setIsDel(false)
    setStatus(null)
    setStatusState(null)
    try {
      axios
        .post("http://127.0.0.1:8000/api/anime/del", {
          anime_id: id_anime,
          user_id: id_user,
        })
        .then((response) => {})
        .catch((error) => {});
    } catch (error) {}
  }

  return (
    <div>
      <div className="rating-component">
        <StatusComponent
          setStatus={setStatus}
          currentUser={currentUser}
          setStatusState={setStatusState}
          setIsDel = {setIsDel}
          status = {status}
        />
        {status === "completed" && (
          <>
            <h4>Установить оценку:</h4>
            <input
              className="slider"
              type="range"
              min="1"
              max="10"
              value={rating}
              onChange={handleRatingChange}
            />
            <p>Ваша оценка: {rating}</p>
          </>
        )}
        {isDel && <div onClick={delObject} className="isDel">Удалить из списка</div>}
      </div>
    </div>
  );
};
export default RatingComponent;
