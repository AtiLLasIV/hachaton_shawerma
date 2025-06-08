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
    // Средняя зарплата по всем вакансиям компании
    const avgSalary = Math.round(
      vacs
        .map(v => v.salary)
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
            <div className="company-salary">Средняя зарплата: <b>{avgSalary.toLocaleString()} ₽</b></div>
          </div>
        ))}
      </div>
    </div>
  );
} 