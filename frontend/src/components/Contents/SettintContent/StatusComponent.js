import React, { useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const StatusComponent = ({ setStatus, currentUser, status, setIsDel, setStatusState }) => {
  const { id } = useParams();

  const [id_user, setId_user] = useState(currentUser.id);
  const [id_anime, setId_anime] = useState(id);

  const handleSubmit = async (Status) => {
    try {
      axios
        .put("http://127.0.0.1:8000/api/score/", {
          anime_id: id_anime,
          user_id: id_user,
          status: Status,
        })
        .then((response) => {})
        .catch((error) => {});
    } catch (error) {}
  };

  const handleStatusChange = (newStatus) => {
    setStatusState(newStatus);
    setStatus(newStatus);
    setIsDel(true)
    handleSubmit(newStatus)
  };

  return (
    <div className="status-component">
      <h4>Установить статус:</h4>
      <div className="card-container">
        <div
          className={`card ${
            status === "completed" ? "selected green" : ""
          }`}
          onClick={() => handleStatusChange("completed")}
        >
          Просмотренно
        </div>
        <div
          className={`card ${status === "watching" ? "selected blue" : ""}`}
          onClick={() => handleStatusChange("watching")}
        >
          Смотрю
        </div>
        <div
          className={`card ${
            status === "planned" ? "selected yl" : ""
          }`}
          onClick={() => handleStatusChange("planned")}
        >
          Запланированно
        </div>
        <div
          className={`card ${status === "dropped" ? "selected red" : ""}`}
          onClick={() => handleStatusChange("dropped")}
        >
          Брошенно
        </div>
      </div>
    </div>
  );
};

export default StatusComponent;
