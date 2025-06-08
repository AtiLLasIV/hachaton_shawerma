#!/usr/bin/env python3
"""
Script to recursively fetch vacancies from hh.ru API (avoiding the 2000-item limit by date-splitting),
filter by regions and employers, and store each vacancy's JSON in a three-letter-hash-based directory.
Additionally, generates a dump file summarizing total found vs extracted.
"""

"""

Usage example: 
python dump_vacancy.py \
  --from_date 2025-05-01 \
  --regions 1 2 \
  --employers 1000 \
  --output_dir hh/
"""

import argparse
import requests
import time
import os
import json
import hashlib
import sys
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser(
        description='Fetch hh.ru vacancies, split by date ranges, filter by regions/employers, save JSON files, and dump results.'
    )
    parser.add_argument(
        '--from_date', type=str, required=True,
        help='Earliest date (YYYY-MM-DD) to fetch vacancies from (inclusive), up to today.'
    )
    parser.add_argument(
        '--regions', type=int, nargs='+', required=True,
        help='List of region IDs (e.g., 1 for Moscow).'
    )
    parser.add_argument(
        '--employers', type=int, nargs='*', default=[],
        help='List of employer IDs to filter by (optional).'
    )
    parser.add_argument(
        '--per_page', type=int, default=100,
        help='Vacancies per page (max 100).'
    )
    parser.add_argument(
        '--pause', type=float, default=0.2,
        help='Pause between API requests, in seconds.'
    )
    parser.add_argument(
        '--output_dir', type=str, default='vacancies',
        help='Base directory to save vacancy JSON files.'
    )
    return parser.parse_args()


def fetch_interval(area_id, employer_id, start_dt, end_dt, per_page, pause, seen, output_dir):
    base_url = 'https://api.hh.ru/vacancies'

    def fetch_range(start, end):
        params = {
            'area': area_id,
            'date_from': start.isoformat(),
            'date_to': end.isoformat(),
            'per_page': per_page,
            'page': 0
        }
        if employer_id is not None:
            params['employer_id'] = employer_id

        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        found = data.get('found', 0)
        pages = data.get('pages', 0)
        max_items = per_page * 100

        if found == 0:
            return

        if found <= max_items:
            for page in range(pages):
                params['page'] = page
                r = requests.get(base_url, params=params)
                r.raise_for_status()
                items = r.json().get('items', [])
                for item in items:
                    raw = json.dumps(item, sort_keys=True, ensure_ascii=False).encode('utf-8')
                    hash_str = hashlib.sha256(raw).hexdigest()
                    if hash_str in seen:
                        continue
                    seen.add(hash_str)
                    prefix = hash_str[:3]
                    dir_path = os.path.join(output_dir, prefix)
                    os.makedirs(dir_path, exist_ok=True)
                    file_path = os.path.join(dir_path, f"{hash_str}.json")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(item, f, ensure_ascii=False, indent=2)
                time.sleep(pause)
        else:
            mid = start + (end - start) / 2
            fetch_range(start, mid)
            fetch_range(mid, end)

    fetch_range(start_dt, end_dt)


def main():
    args = parse_args()

    try:
        start_dt = datetime.fromisoformat(args.from_date)
    except ValueError:
        sys.exit("Error: --from_date must be in YYYY-MM-DD format.")
    end_dt = datetime.now()

    combos = []
    for region in args.regions:
        if args.employers:
            for emp in args.employers:
                combos.append((region, emp))
        else:
            combos.append((region, None))

    total_found = 0
    base_url = 'https://api.hh.ru/vacancies'
    for region, emp in combos:
        params = {
            'area': region,
            'date_from': start_dt.isoformat(),
            'date_to': end_dt.isoformat()
        }
        if emp is not None:
            params['employer_id'] = emp
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        total_found += resp.json().get('found', 0)

    os.makedirs(args.output_dir, exist_ok=True)
    seen = set()
    for region, emp in combos:
        fetch_interval(
            area_id=region,
            employer_id=emp,
            start_dt=start_dt,
            end_dt=end_dt,
            per_page=args.per_page,
            pause=args.pause,
            seen=seen,
            output_dir=args.output_dir
        )

    total_saved = len(seen)
    hash_input = f"{args.from_date}{args.regions}{args.employers}{end_dt.isoformat()}"
    dump_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:8]
    dump_filename = f"dump_res_{dump_hash}.txt"
    with open(dump_filename, 'w', encoding='utf-8') as df:
        df.write(f"Total vacancies found for period {args.from_date} to {end_dt.isoformat()}: {total_found}\n")
        df.write(f"Total unique vacancies saved: {total_saved}\n")

if __name__ == '__main__':
    main()
