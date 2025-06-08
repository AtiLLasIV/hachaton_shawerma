from db.connect import get_db_connection

def get_vacancies(filters):
    conn = get_db_connection()
    cur = conn.cursor()
    where = []
    values = []
    for key, value in filters.items():
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