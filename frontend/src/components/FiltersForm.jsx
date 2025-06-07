import React, { useState } from "react";
import "./FiltersForm.css";

export function FiltersForm({ onSubmit }) {
  const [position, setPosition] = useState("");
  const [region, setRegion] = useState("");
  const [experience, setExperience] = useState("");
  const [gender, setGender] = useState("");
  const [age, setAge] = useState("");
  const [hasCar, setHasCar] = useState(false);
  const [sources, setSources] = useState([]);

  const handleCheckboxChange = (source) => {
    setSources(prev =>
      prev.includes(source)
        ? prev.filter(s => s !== source)
        : [...prev, source]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      position,
      region,
      experience: experience ? parseFloat(experience) : null,
      gender,
      age: age ? parseInt(age) : null,
      hasCar,
      sources
    });
  };

  return (
    <form onSubmit={handleSubmit} className="filters-form">
      <div className="form-section">
        <label>
          Должность:
        </label>
        <input
          type="text"
          value={position}
          onChange={(e) => setPosition(e.target.value)}
          placeholder="Курьер"
        />
      </div>

      <div className="form-section">
        <label>
          Регион:
        </label>
        <input
          type="text"
          value={region}
          onChange={(e) => setRegion(e.target.value)}
          placeholder="Москва"
        />
      </div>

      <div className="form-section">
        <label>
          Опыт (лет):
        </label>
        <input
          type="number"
          step="0.5"
          min="0"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          placeholder="1,5"
        />
      </div>

      <div className="form-section">
        <label>
          Пол:
        </label>
        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option value="male">Мужской</option>
          <option value="female">Женский</option>
        </select>
      </div>

      <div className="form-section">
        <label>
          Возраст:
        </label>
        <input
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          placeholder="25"
        />
      </div>

      <div className="form-section">
        <label>
          <input
            type="checkbox"
            checked={hasCar}
            onChange={(e) => setHasCar(e.target.checked)}
          />
          Наличие автомобиля
        </label>
      </div>

      <div className="form-section">
        <label>Источники:</label>
        <label><input type="checkbox" checked={sources.includes("hh")} onChange={() => handleCheckboxChange("hh")} /> hh.ru</label>
        <label><input type="checkbox" checked={sources.includes("avito")} onChange={() => handleCheckboxChange("avito")} /> Avito</label>
        <label><input type="checkbox" checked={sources.includes("tg")} onChange={() => handleCheckboxChange("tg")} /> Telegram</label>
      </div>

      <button type="submit">Мониторить</button>
    </form>
  );
}