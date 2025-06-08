import React, { useEffect, useState } from 'react';
import { SummaryBlock } from '../components/SummaryBlock';
import { CompanyVacancySummary } from '../components/CompanyVacancySummary';
import { getVacancies } from '../api/apiService';

export default function SummaryPage() {
  const [vacancies, setVacancies] = useState([]);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    async function fetchData() {
      // Получаем параметры фильтрации из localStorage
      const searchParams = JSON.parse(localStorage.getItem('searchParams') || '{}');
      const data = await getVacancies(searchParams);
      setVacancies(data);

      const salaries = data
        .map(v => v.salary)
        .filter(Boolean)
        .sort((a, b) => a - b);

      if (!salaries.length) return;

      const count = salaries.length;
      const avg = Math.round(salaries.reduce((a, b) => a + b, 0) / count);
      const median = salaries[Math.floor(count / 2)];
      const min = salaries[0];
      const max = salaries[count - 1];

      setSummary({
        count,
        average: avg,
        median,
        min,
        max,
        avgRange: avg, 
      });
    }

    fetchData();
  }, []);

  return (
    <div style={{ padding: '32px' }}>
      {summary && <SummaryBlock {...summary} />}
      <CompanyVacancySummary vacancies={vacancies} />
    </div>
  );
}
