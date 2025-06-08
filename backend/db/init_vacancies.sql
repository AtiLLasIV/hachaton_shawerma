CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    company VARCHAR(128),
    position VARCHAR(128),
    city VARCHAR(64),
    experience_years INT,
    salary INT,
    currency VARCHAR(8),
    posted_at TIMESTAMP,
); 
