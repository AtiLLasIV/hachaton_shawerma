import React, { useState } from "react";
import { FiltersForm } from "../components/FiltersForm";
import { runMonitoring } from "../api/apiService";
// import { SummaryBlock } from "../components/SummaryBlock"; // будет позже

export function MonitorPage() {
  const [result, setResult] = useState(null);

  const handleSubmit = async (params) => {
    const data = await runMonitoring(params);
    setResult(data);
  };

  return (
    <div>
      <h2>Мониторинг вакансий</h2>
      <FiltersForm onSubmit={handleSubmit} />

      {result && (
        <pre>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}

      {/* {result && <SummaryBlock {...result} />} */}
    </div>
  );
}