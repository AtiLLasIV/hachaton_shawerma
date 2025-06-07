import React from 'react';
import './CompanyVacancySummary.css';

function getCompanyStats(vacancies) {
  // Группировка по компании
  const companies = {};
  vacancies.forEach(vac => {
    const company = vac.company || 'Без названия';
    if (!companies[company]) companies[company] = [];
    companies[company].push(vac);
  });
  // Формируем массив для рендера
  return Object.entries(companies).map(([company, vacs]) => {
    // Средняя вилка по всем вакансиям компании
    const avgSalary = Math.round(
      vacs
        .map(v => normalizeSalary(v.salary_from, v.salary_to))
        .filter(Boolean)
        .reduce((a, b) => a + b, 0) / vacs.length
    );
    return {
      company,
      avgSalary,
      positions: vacs.map(v => v.position)
    };
  });
}

function normalizeSalary(from, to) {
  if (from && to) return (from + to) / 2;
  if (from) return from * 1.15;
  if (to) return to * 0.85;
  return null;
}

export function CompanyVacancySummary({ vacancies }) {
  const stats = getCompanyStats(vacancies);
  return (
    <div className="company-summary-list">
      <h3 className="company-summary-title">Сводка по компаниям</h3>
      <div className="company-summary-grid">
        {stats.map(({ company, avgSalary, positions }) => (
          <div className="company-card" key={company}>
            <div className="company-card-header">
              <span className="company-name">{company}</span>
            </div>
            <div className="company-positions">
              {positions.map((pos, idx) => (
                <div className="company-position" key={idx}>{pos}</div>
              ))}
            </div>
            <div className="company-salary">Средняя вилка: <b>{avgSalary.toLocaleString()} ₽</b></div>
          </div>
        ))}
      </div>
    </div>
  );
} 