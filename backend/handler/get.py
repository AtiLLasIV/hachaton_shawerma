from db.connect import get_db_connection

from sentence_transformers import SentenceTransformer
import joblib
import json

# Предзагрузка моделей и данных
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
PCA = joblib.load('pca.joblib')
with open('out.txt', 'r', encoding='utf-8') as f:
    CLUSTERS = json.load(f)
CENTERS = [c['cluster_emb'] for c in CLUSTERS]


def get_cluster_name(title: str) -> str:
    """Возвращает название кластера для заголовка вакансии"""
    emb = MODEL.encode([title], convert_to_numpy=True)
    emb_reduced = PCA.transform(emb)

    # Поиск ближайшего центра
    dists = [(i, ((center - emb_reduced) ** 2).sum() ** 0.5)
             for i, center in enumerate(CENTERS)]
    idx, _ = min(dists, key=lambda x: x[1])
    return CLUSTERS[idx]['cluster_name']

def get_vacancies(filters):
    conn = get_db_connection()
    cur = conn.cursor()
    where = []
    values = []
    allowed_fields = {'company', 'position', 'city', 'experience_years', 'salary', 'currency', 'posted_at'}
    print(filters)
    for key, value in filters.items():
        print(key, value)
        if key in allowed_fields:
            if key == "position":
                value = get_cluster_name(value)
            if key == "region":
                key = "city"
            where.append(f"{key} = %s")
            values.append(value)
    where_clause = " AND ".join(where) if where else "1=1"
    cur.execute(f"SELECT * FROM vacancies WHERE {where_clause}", values)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows] 


# МОК ДАННЫЕ ДЛЯ ТЕСТА СЕРВЕРА

# def get_vacancies(filters):
#     # Возвращаем список фиктивных вакансий
#     return [
#         {
#             "id": 1,
#             "company": "Самокат",
#             "position": "Курьер",
#             "city": "Москва",
#             "salary_min_net": 50000,
#             "salary_max_net": 70000
#         },
#         {
#             "id": 2,
#             "company": "Яндекс Еда",
#             "position": "Курьер",
#             "city": "Санкт-Петербург",
#             "salary_min_net": 60000,
#             "salary_max_net": 80000
#         }
#     ]