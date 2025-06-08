import React from "react";
import { FiltersForm } from "../components/FiltersForm";
import { useNavigate } from "react-router-dom";

export function MonitorPage() {

  const navigate = useNavigate();

  const handleSubmit = async (params) => {
    try {
      navigate("/summary");
    } catch (e) {
      console.error("Ошибка при мониторинге", e);
    }
  };

  return (
    <div>
      <FiltersForm onSubmit={handleSubmit}/>
    </div>
  );
}