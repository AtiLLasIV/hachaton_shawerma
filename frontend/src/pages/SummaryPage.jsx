import React, { useEffect, useState } from 'react';
import { SummaryBlock } from '../components/SummaryBlock';
import { CompanyVacancySummary } from '../components/CompanyVacancySummary';
import { getMockVacancies } from '../api/apiService';

export default function SummaryPage() {
  const [vacancies, setVacancies] = useState([]);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const data = await getMockVacancies();
      setVacancies(data);

      const salaries = data
        .map(v => normalizeSalary(v.salary_from, v.salary_to))
        .filter(Boolean)
        .sort((a, b) => a - b);

      if (!salaries.length) return;

      const count = salaries.length;
      const avg = Math.round(salaries.reduce((a, b) => a + b, 0) / count);
      const median = salaries[Math.floor(count / 2)];
      const min = salaries[0];
      const max = salaries[count - 1];
      const avgRange = salaries.filter((_, i) => data[i]?.salary_from && data[i]?.salary_to)
        .map((v, i) => normalizeSalary(data[i].salary_from, data[i].salary_to))
        .reduce((a, b) => a + b, 0) / count;

      setSummary({
        count,
        average: avg,
        median,
        min,
        max,
        avgRange: Math.round(avgRange),
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

function normalizeSalary(from, to) {
  if (from && to) return (from + to) / 2;
  if (from) return from * 1.15;
  if (to) return to * 0.85;
  return null;
}
