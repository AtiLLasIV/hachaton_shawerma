from db.connect import get_db_connection

# def insert_vacancy(data):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """INSERT INTO vacancies (company, position, city, experience_years, salary, currency, posted_at)
#         VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
#         (
#             data.get('company'),
#             data.get('position'),
#             data.get('city'),
#             data.get('experience_years'),
#             data.get('salary'),
#             data.get('currency'),
#             data.get('posted_at')
#         )
#     )
#     conn.commit()
#     new_id = cur.fetchone()[0]
#     cur.close()
#     conn.close()
#     return {"id": new_id, "status": "ok"} 

# МОК ДАННЫЕ ДЛЯ ТЕСТА СЕРВЕРА


def insert_vacancy(data):
    # Просто возвращаем, что всё ок (без БД)
    return {"id": 1, "status": "ok", "mock": True}