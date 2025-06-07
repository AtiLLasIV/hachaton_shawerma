import React, { useState } from "react";
import ReactSlider from "react-slider"; // [добавлено] импорт ползунка
import "./Slider.css"; //
import "./FiltersForm.css";

export function FiltersForm({ onSubmit }) {
  const [position, setPosition] = useState("");
  const [region, setRegion] = useState("");
  const [experienceRange, setExperienceRange] = useState([0, 20]); // [изменено] диапазон вместо одного числа
  const [gender, setGender] = useState("");
  const [age, setAge] = useState({ from: "", to: "" });
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
      experience_from: experienceRange[0], // [добавлено]
      experience_to: experienceRange[1] === 20 ? 99 : experienceRange[1], // здесь не забыть про бэк
      gender,
      age_from: age.from ? parseInt(age.from) : null,
      age_to: age.to ? parseInt(age.to) : null,
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

      <div className="form-section slider-section">
        <label>Опыт (лет):</label>

        {/* верхняя подпись (0 и 20+) */}
        <div style={{display: "flex", justifyContent: "space-between", fontSize: "0.85rem", color: "#888"}}>
          <span>0</span>
          <span>20+</span>
        </div>

        <ReactSlider
          className="horizontal-slider"
          thumbClassName="exp-thumb"
          renderTrack={(props, state) => (
            <div {...props} className={`exp-track-${state.index}`}/>
          )}
          min={0}
          max={20}
          step={0.5}
          value={experienceRange}
          onChange={setExperienceRange}
          pearling
          minDistance={0.5}
          renderThumb={(props, state, index) => (
            <div {...props}>
              <div className="exp-thumb-label">
                {state.valueNow === 20 ? "20+" : state.valueNow}
              </div>
            </div>
          )}
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
        <label>Возраст:</label>
        <div className="age-inputs-row">
          <input
            type="number"
            min="0"
            placeholder="От"
            value={age.from}
            onChange={(e) => setAge({...age, from: e.target.value})}
          />
          <input
            type="number"
            min="0"
            placeholder="До"
            value={age.to}
            onChange={(e) => setAge({...age, to: e.target.value})}
          />
        </div>
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
        <label><input type="checkbox" checked={sources.includes("hh")}
                      onChange={() => handleCheckboxChange("hh")}/> hh.ru</label>
        <label><input type="checkbox" checked={sources.includes("avito")}
                      onChange={() => handleCheckboxChange("avito")}/> Avito</label>
        <label><input type="checkbox" checked={sources.includes("tg")}
                      onChange={() => handleCheckboxChange("tg")}/> Telegram</label>
      </div>

      <button type="submit">Мониторить</button>
    </form>
  );
}