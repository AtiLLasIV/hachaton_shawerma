from db.connect import get_db_connection

# def get_aggregates(filters):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     where = []
#     values = []
#     for key, value in filters.items():
#         where.append(f"{key} = %s")
#         values.append(value)
#     where_clause = " AND ".join(where) if where else "1=1"
#     cur.execute(f'''
#         SELECT
#             percentile_cont(0.5) WITHIN GROUP (ORDER BY salary) AS median,
#             percentile_cont(0.25) WITHIN GROUP (ORDER BY salary) AS q1,
#             percentile_cont(0.75) WITHIN GROUP (ORDER BY salary) AS q3,
#             avg(salary) as avg_salary
#         FROM vacancies
#         WHERE {where_clause}
#     ''', values)
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     return {
#         "median": result[0],
#         "q1": result[1],
#         "q3": result[2],
#         "avg": result[3]
#     } 

# МОК ДАННЫЕ ДЛЯ ТЕСТА СЕРВЕРА


def get_aggregates(filters):
    # Возвращаем фиктивную агрегацию
    return {
        "median": 65000,
        "q1": 55000,
        "q3": 75000,
        "avg": 65000
    }