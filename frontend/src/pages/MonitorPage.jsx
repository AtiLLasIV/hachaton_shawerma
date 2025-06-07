import React from "react";
import { FiltersForm } from "../components/FiltersForm";
import { runMonitoring } from "../api/apiService";
import { useNavigate } from "react-router-dom";

export function MonitorPage() {

  const navigate = useNavigate();

  const handleSubmit = async (params) => {
    try {
      const data = await runMonitoring(params);
      navigate("/summary", { state: { result: data } });
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