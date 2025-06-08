from db.connect import get_db_connection
from collections import defaultdict
from sentence_transformers import SentenceTransformer
import joblib
import json
import numpy as np

# Предзагрузка моделей и данных
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
PCA = joblib.load('pca.joblib')
with open('out.txt', 'r', encoding='utf-8') as f:
    CLUSTERS = json.load(f)
CENTERS = [c['cluster_emb'] for c in CLUSTERS]

def get_vacancy_embedding(vacancy_text):
    """Получение эмбеддинга для текста вакансии"""
    embedding = MODEL.encode(vacancy_text)
    return PCA.transform(embedding.reshape(1, -1))[0]

def find_closest_cluster(embedding):
    """Поиск ближайшего кластера для эмбеддинга"""
    distances = [np.linalg.norm(embedding - center) for center in CENTERS]
    return np.argmin(distances)

def get_vacancies(filters):
    conn = get_db_connection()
    cur = conn.cursor()
    where = []
    values = []
    allowed_fields = {'company', 'position', 'city', 'experience_years', 'salary', 'currency', 'posted_at'}
    
    # Добавляем фильтры
    for key, value in filters.items():
        if key in allowed_fields:
            where.append(f"{key} = %s")
            values.append(value)
    
    where_clause = " AND ".join(where) if where else "1=1"
    
    # Получаем все вакансии
    cur.execute(f"SELECT * FROM vacancies WHERE {where_clause}", values)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    
    # Преобразуем строки в словари
    all_vacancies = [dict(zip(columns, row)) for row in rows]
    
    # Получаем вашу вакансию (предполагаем, что она первая в списке или имеет специальный флаг)
    your_vacancy = all_vacancies[0] if all_vacancies else None
    other_vacancies = all_vacancies[1:] if all_vacancies else []
    
    # Если есть ваша вакансия, получаем её эмбеддинг и кластер
    if your_vacancy:
        vacancy_text = f"{your_vacancy['position']} {your_vacancy.get('description', '')}"
        embedding = get_vacancy_embedding(vacancy_text)
        cluster_id = find_closest_cluster(embedding)
        your_vacancy['cluster_id'] = int(cluster_id)
    
    # Группируем остальные вакансии по названию должности
    grouped_vacancies = defaultdict(list)
    for vacancy in other_vacancies:
        position = vacancy.get('position', '').strip()
        if position:
            grouped_vacancies[position].append(vacancy)
    
    # Формируем результат
    result = {
        'your_vacancy': your_vacancy,
        'grouped_vacancies': []
    }
    
    for position, vacancies in grouped_vacancies.items():
        result['grouped_vacancies'].append({
            'position': position,
            'count': len(vacancies),
            'vacancies': vacancies
        })
    
    # Сортируем по количеству вакансий (по убыванию)
    result['grouped_vacancies'].sort(key=lambda x: x['count'], reverse=True)
    
    cur.close()
    conn.close()
    return result

# МОК ДАННЫЕ ДЛЯ ТЕСТА СЕРВЕРА

# def get_vacancies(filters):
#     # Возвращаем список сгруппированных фиктивных вакансий
#     return {
#         "your_vacancy": {
#             "id": 1,
#             "company": "Ваша компания",
#             "position": "Ваша вакансия",
#             "city": "Москва",
#             "salary_min_net": 100000,
#             "salary_max_net": 150000,
#             "cluster_id": 0
#         },
#         "grouped_vacancies": [
#             {
#                 "position": "Курьер",
#                 "count": 2,
#                 "vacancies": [
#                     {
#                         "id": 2,
#                         "company": "Самокат",
#                         "position": "Курьер",
#                         "city": "Москва",
#                         "salary_min_net": 50000,
#                         "salary_max_net": 70000
#                     },
#                     {
#                         "id": 3,
#                         "company": "Яндекс Еда",
#                         "position": "Курьер",
#                         "city": "Санкт-Петербург",
#                         "salary_min_net": 60000,
#                         "salary_max_net": 80000
#                     }
#                 ]
#             }
#         ]
#     }