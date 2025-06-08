from db.connect import get_db_connection

def insert_vacancy(data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO vacancies (company, position, city, salary_min_net, salary_max_net)
        VALUES (%s, %s, %s, %s, %s) RETURNING id""",
        (data.get('company'), data.get('position'), data.get('city'), data.get('salary_min_net'), data.get('salary_max_net'))
    )
    conn.commit()
    new_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"id": new_id, "status": "ok"} 

# МОК ДАННЫЕ ДЛЯ ТЕСТА СЕРВЕРА


# def insert_vacancy(data):
#     # Просто возвращаем, что всё ок (без БД)
#     return {"id": 1, "status": "ok", "mock": True}