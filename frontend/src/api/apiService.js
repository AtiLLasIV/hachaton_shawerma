
const API_URL = "http://10.10.165.2:5001";


// export async function getMockVacancies() {
//     const res = await fetch("http://127.0.0.1:5001/mock_vacancies");
//     return res.json();
//   }

export async function getVacancies(filters = {}) {
  const params = new URLSearchParams(filters).toString();
  const res = await fetch(`${API_URL}/vacancies?${params}`);
  return res.json();
}

export async function addVacancy(data) {
  const res = await fetch(`${API_URL}/vacancy`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function getAggregates(filters = {}) {
  const params = new URLSearchParams(filters).toString();
  const res = await fetch(`${API_URL}/vacancies/aggregate?${params}`);
  return res.json();
}
