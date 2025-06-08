from db.connect import get_db_connection
from psycopg2 import sql

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

    conditions = []
    values = []
    allowed_fields = {'company', 'position', 'city', 'experience_years', 'salary', 'currency', 'posted_at'}

    exp_to = 1000
    exp_from = 0

    for key, value in filters.items():
        if key == "experience_from":
            exp_from = value
        elif key == "experience_to":
            exp_to = value
        elif key == "region":
            key = "city"

        if key in allowed_fields:
            if key == "position":
                value = get_cluster_name(value)
            conditions.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
            values.append(value)

    # Добавляем условие по опыту, если указаны границы
    if 'experience_from' in filters or 'experience_to' in filters:
        conditions.append(sql.SQL("experience_years BETWEEN %s AND %s"))
        values.extend([exp_from, exp_to])

    # Формируем базовый запрос
    query = sql.SQL("SELECT * FROM vacancies")

    # Добавляем условия, если они есть
    if conditions:
        query = sql.SQL("{} WHERE {}").format(
            query,
            sql.SQL(" AND ").join(conditions)
        )

    query = sql.SQL("{} ORDER BY company DESC").format(query)

    print(query.as_string(conn), values)

    try:
        cur.execute(query, tuple(values))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cur.close()
        conn.close()

    return [dict(zip(columns, row)) for row in rows]