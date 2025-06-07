#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import joblib
import sys

import numpy as np
from sentence_transformers import SentenceTransformer

def main():
    parser = argparse.ArgumentParser(description='Нахождение кластера для одного заголовка')
    parser.add_argument('title', help='Текст заголовка вакансии')
    parser.add_argument('--pca-file', default="pca.joblib", help='Файл с сохранённым PCA (joblib)')
    parser.add_argument('--clusters-file', required=True, help='JSON с центрами кластеров')
    parser.add_argument('--out', required=True, help='Файл, куда записать результат (имя кластера)')
    args = parser.parse_args()

    # Загрузка PCA и центров кластеров
    try:
        pca = joblib.load(args.pca_file)
    except Exception as e:
        print(f"Ошибка загрузки PCA из {args.pca_file}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.clusters_file, 'r', encoding='utf-8') as f:
            clusters = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения кластеров из {args.clusters_file}: {e}", file=sys.stderr)
        sys.exit(1)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb = model.encode([args.title], convert_to_numpy=True)
    emb_reduced = pca.transform(emb)

    centers = np.array([c['cluster_emb'] for c in clusters])
    dists = np.linalg.norm(centers - emb_reduced, axis=1)
    idx = np.argmin(dists)
    nearest = clusters[idx]['cluster_name']

    try:
        with open(args.out, 'w', encoding='utf-8') as fo:
            fo.write(nearest)
    except Exception as e:
        print(f"Ошибка записи в {args.out}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
