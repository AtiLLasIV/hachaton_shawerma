export async function getMockVacancies() {
  return [
    {
      company: 'РоссияАвто',
      position: 'Курьер',
      salary_from: 40000,
      salary_to: 42000,
      region: 'Москва',
      employment_type: 'Full time',
      posted_at: '2024-06-10T10:00:00Z',
      company_logo: 'https://randomuser.me/api/portraits/men/32.jpg',
      source: 'hh',
    },
    {
      company: 'Самокат',
      position: 'Курьер на велосипеде',
      salary_to: 193000,
      region: 'Москва',
      employment_type: 'Частичная занятость',
      posted_at: '2024-06-09T09:00:00Z',
      company_logo: 'https://randomuser.me/api/portraits/men/33.jpg',
      source: 'avito',
    },
    {
      company: 'Яндекс Еда',
      position: 'Курьер',
      salary_from: 70000,
      salary_to: 90000,
      region: 'Санкт-Петербург',
      employment_type: 'Full time',
      posted_at: '2024-06-08T12:00:00Z',
      company_logo: 'https://randomuser.me/api/portraits/women/44.jpg',
      source: 'tg',
    },
    {
      company: 'Самокат',
      position: 'Курьер на авто',
      salary_from: 100000,
      salary_to: 130000,
      region: 'Москва',
      employment_type: 'Full time',
      posted_at: '2024-06-06T11:00:00Z',
      company_logo: 'https://randomuser.me/api/portraits/men/33.jpg',
      source: 'avito',
    },
  ];
}
  