import React from 'react';
import './SummaryBlock.css';

export function SummaryBlock({ count, average, median, min, max, avgRange }) {
  return (
    <div className="summary-container">
      <h2>📊 Сводка по результатам</h2>
      <div className="summary-grid">
        <div className="summary-card">
          <span className="label">Вакансий:</span>
          <span className="value">{count}</span>
        </div>
        <div className="summary-card">
          <span className="label">Средняя ЗП:</span>
          <span className="value">{average.toLocaleString()} ₽</span>
        </div>
        <div className="summary-card">
          <span className="label">Медианная ЗП:</span>
          <span className="value">{median.toLocaleString()} ₽</span>
        </div>
        <div className="summary-card">
          <span className="label">Мин / Макс ЗП:</span>
          <span className="value">
            {min.toLocaleString()} ₽ / {max.toLocaleString()} ₽
          </span>
        </div>
        <div className="summary-card">
          <span className="label">Средняя вилка:</span>
          <span className="value">{avgRange.toLocaleString()} ₽</span>
        </div>
      </div>
    </div>
  );
}
