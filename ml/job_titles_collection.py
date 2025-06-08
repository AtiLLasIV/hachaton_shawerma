import requests
import time
from datetime import datetime, timedelta


def fetch_vacancy_names_interval(area_id, start_dt, end_dt, per_page=100, pause=0.2, seen=None, output_file=None):
    """
    Рекурсивно собирает и сразу записывает названия вакансий из hh.ru для заданной области,
    обходя ограничение в 2000 записей через фильтрацию по диапазону дат.

    :param area_id: int, ID региона (1 — Москва)
    :param start_dt: datetime, начало периода (вкл.)
    :param end_dt: datetime, конец периода (вкл.)
    :param per_page: int, вакансий на страницу (макс. 100)
    :param pause: float, задержка между запросами
    :param seen: set, множество уже записанных названий
    :param output_file: str, путь к файлу для записи результатов
    """
    base_url = "https://api.hh.ru/vacancies"

    def fetch_interval(start, end):
        iso_start = start.isoformat()
        iso_end = end.isoformat()
        print(f"Fetching from {iso_start} to {iso_end}")
        params = {
            "area": area_id,
            "per_page": per_page,
            "page": 0,
            "date_from": iso_start,
            "date_to": iso_end
        }
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        found = data.get("found", 0)
        pages = data.get("pages", 0)
        max_items = per_page * 100
        print(f"  Found {found} vacancies, pages={pages}")

        if found == 0:
            return
        if found <= max_items:
            for page in range(pages):
                params["page"] = page
                r = requests.get(base_url, params=params)
                r.raise_for_status()
                items = r.json().get("items", [])
                # Запись результатов
                with open(output_file, "a", encoding="utf-8") as f:
                    for item in items:
                        name = item.get("name", "").strip()
                        if name and name not in seen:
                            f.write(name + "\n")
                            seen.add(name)
                print(f"    Page {page+1}/{pages}: wrote {len(items)} items")
                time.sleep(pause)
        else:
            mid = start + (end - start) / 2
            fetch_interval(start, mid)
            fetch_interval(mid, end)

    fetch_interval(start_dt, end_dt)


def main():
    output_file = "vacancies_names.txt"
    open(output_file, "w", encoding="utf-8").close()

    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=30)

    # Для удаления дубликатов
    seen = set()

    # Сбор и запись вакансий Москвы
    fetch_vacancy_names_interval(
        area_id=1,
        start_dt=start_dt,
        end_dt=end_dt,
        per_page=100,
        pause=0.2,
        seen=seen,
        output_file=output_file
    )

    print(f"Total vacancies written: {len(seen)}")
    print(f"Результаты постепенно записаны в файл: {output_file}")

if __name__ == "__main__":
    main()
