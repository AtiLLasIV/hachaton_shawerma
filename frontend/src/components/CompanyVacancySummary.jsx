import React from 'react';
import './CompanyVacancySummary.css';

function getCompanyStats(vacancies) {
  const companies = {};

  vacancies.forEach(vac => {
    const company = vac.company || 'Без названия';
    const position = vac.position || 'Без должности';

    if (!companies[company]) companies[company] = { totalSalary: 0, count: 0, positions: {} };

    companies[company].totalSalary += vac.salary || 0;
    companies[company].count += 1;

    if (!companies[company].positions[position]) {
      companies[company].positions[position] = 0;
    }
    companies[company].positions[position] += 1;
  });

  return Object.entries(companies).map(([company, data]) => {
    const avgSalary = Math.round(data.totalSalary / data.count);
    const positionStats = Object.entries(data.positions).map(
      ([position, count]) => ({ position, count })
    );
    return {
      company,
      avgSalary,
      positionStats
    };
  });
}

export function CompanyVacancySummary({ vacancies }) {
  const stats = getCompanyStats(vacancies);
  return (
    <div className="company-summary-list">
      <h3 className="company-summary-title">Сводка по компаниям</h3>
      <div className="company-summary-grid">
        {stats.slice(0, 10).map(({ company, avgSalary, positionStats }) => (
          <div className="company-card" key={company}>
            <div className="company-card-header">
              <span className="company-name">{company}</span>
            </div>
            <div className="company-positions">
              {positionStats.map(({ position, count }, idx) => (
                <div className="company-position" key={idx}>
                  {position} — {count} вакансии{count === 1 ? 'я' : count < 5 ? 'и' : ''}
                </div>
              ))}
            </div>
            <div className="company-salary">
              Средняя зарплата: <b>{avgSalary.toLocaleString()} ₽</b>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}