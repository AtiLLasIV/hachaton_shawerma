
const API_URL = "http://10.10.165.2:5001";


// export async function getMockVacancies() {
//     const res = await fetch("http://127.0.0.1:5001/mock_vacancies");
//     return res.json();
//   }

export async function getVacancies(filters = {}) {
  try {
    const params = new URLSearchParams();
    // Добавляем только непустые параметры
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });
    
    const res = await fetch(`${API_URL}/vacancies?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json();
  } catch (error) {
    console.error('Error fetching vacancies:', error);
    return [];
  }
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
